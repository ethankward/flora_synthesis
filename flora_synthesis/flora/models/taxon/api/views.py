from django.db import transaction
from django.db.models import Prefetch
from rest_framework import viewsets, views, status
from rest_framework.decorators import api_view
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from flora import models
from flora.management.commands import update_computed_values
from flora.models.taxon.api import serializers
from flora.models.taxon.choices import (
    taxon_endemic_statuses,
    taxon_life_cycles,
    taxon_introduced_statuses,
    taxon_ranks,
)


class TaxonViewSet(viewsets.ModelViewSet, UpdateModelMixin):
    queryset = models.Taxon.objects.all()
    serializer_class = serializers.TaxonSerializer

    def get_queryset(self):
        result = (
            models.Taxon.objects.all()
                .prefetch_related("subtaxa", "taxonsynonym_set")
                .select_related("parent_species")
        )

        checklist_id = self.request.query_params.get("checklist", None)
        genus = self.request.query_params.get("genus", None)
        family = self.request.query_params.get("family", None)

        if checklist_id is not None:
            pf = Prefetch(
                "taxon_checklist_taxa",
                queryset=models.ChecklistTaxon.objects.filter(checklist=checklist_id),
            )
            result = result.filter(taxon_checklist_taxa__checklist=checklist_id)
            result = result.prefetch_related(pf)
        else:
            result = result.prefetch_related("taxon_checklist_taxa")

        result = result.prefetch_related(
            "taxon_checklist_taxa__checklist",
            "taxon_checklist_taxa__all_mapped_taxa",
            "taxon_checklist_taxa__family",
        )
        if genus is not None:
            result = result.filter(genus=genus)

        if family is not None:
            result = result.filter(family=family)

        result = result.distinct()
        result = result.order_by("family", "taxon_name")

        return result


class PrimaryChecklistTaxonViewSet(viewsets.ModelViewSet):
    queryset = models.Taxon.objects.all()
    serializer_class = serializers.MinimalTaxonSerializer

    def get_queryset(self):
        result = models.Taxon.objects.all().order_by("taxon_name")
        result = result.filter(
            taxon_checklist_taxa__checklist__primary_checklist=True
        ).distinct()
        return result


class TaxonAutocompleteViewSet(viewsets.ModelViewSet):
    queryset = models.Taxon.objects.all()
    serializer_class = serializers.TaxonNameSerializer

    def get_queryset(self):
        result = models.Taxon.objects.all().order_by("taxon_name")
        search_term = self.request.query_params.get("search_term", None)

        if search_term is not None:
            result = result.filter(taxon_name__icontains=search_term)

        return result


class FamiliesListView(views.APIView):
    def get(self, request):
        data = (
            models.Taxon.objects.all()
                .filter(taxon_checklist_taxa__checklist__primary_checklist=True)
                .order_by("family")
                .values_list("family")
                .distinct()
        )
        result = [{"family": family[0], 'id': i} for (i, family) in enumerate(data)]
        return Response(
            serializers.TaxonFamilySerializer(
                result, many=True
            ).data
        )


class LifeCycleView(views.APIView):
    def get(self, request):
        data = taxon_life_cycles.LifeCycleChoices.choices
        result = [{"id": i, "value": choice[0], "display": choice[1]} for (i, choice) in enumerate(data)]

        return Response(
            serializers.LifeCycleSerializer(
                result, many=True
            ).data
        )


class EndemicView(views.APIView):
    def get(self, request):
        data = taxon_endemic_statuses.EndemicChoices.choices
        result = [{"id": i, "value": choice[0], "display": choice[1]} for (i, choice) in enumerate(data)]

        return Response(
            serializers.EndemicSerializer(
                result, many=True
            ).data
        )


class IntroducedView(views.APIView):
    def get(self, request):
        data = taxon_introduced_statuses.IntroducedChoices.choices
        result = [{"id": i, "value": choice[0], "display": choice[1]} for (i, choice) in enumerate(data)]

        return Response(
            serializers.IntroducedSerializer(
                result, many=True
            ).data
        )


class RankChoicesView(views.APIView):
    def get(self, request):
        data = taxon_ranks.TaxonRankChoices.choices
        return Response(
            serializers.IntroducedSerializer(
                [{"value": i[0], "display": i[1]} for i in data], many=True
            ).data
        )


@api_view(["POST"])
def make_synonym_of(request):
    if request.method != "POST":
        return

    taxon_id_1 = request.data["taxon_id_1"]
    taxon_id_2 = request.data["taxon_id_2"]

    taxon_1 = models.Taxon.objects.get(pk=taxon_id_1)
    taxon_2 = models.Taxon.objects.get(pk=taxon_id_2)

    synonym = models.TaxonSynonym(synonym=taxon_1.taxon_name, taxon=taxon_2)
    with transaction.atomic():
        synonym.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def do_update(request):
    update_computed_values.run()

    return Response(status=status.HTTP_200_OK)

import datetime

from django.core.management import BaseCommand

from flora import models
from django.db import transaction

class Collector:
    def __init__(self, name, aliases=None, urls=None):
        self.name = name
        if aliases is None:
            aliases = []
        self.aliases = sorted(set(aliases + [name]))
        self.urls = urls or []
        self.collections = []

    def __str__(self):
        return 'Collector(name="{}", aliases={}, urls={})'.format(self.name, self.aliases, self.urls)

    __repr__ = __str__

    def add_record(self, record):
        self.collections.append(record)

    def _canonicalize(self, s):
        return s.replace(' ', '').replace('.', '').lower()

    def matches(self, other):
        s1 = self._canonicalize(other)
        for alias in self.aliases:
            if self._canonicalize(alias) == s1:
                return True
        return False

    @property
    def ordered_collections(self):
        return sorted(self.collections, key=lambda x: [x.collection_date, datetime.date.min][x.collection_date is None])

    @property
    def n_collections(self):
        return len(self.collections)

    @property
    def first_date_active(self):
        l = [c.collection_date for c in self.collections if c.collection_date is not None]
        if l:
            return min(l)

    @property
    def last_date_active(self):
        l = [c.collection_date for c in self.collections if c.collection_date is not None]
        if l:
            return max(l)

    @property
    def url(self):
        if self.urls:
            return self.urls[0]


ALL_COLLECTORS = [
    Collector(name="A A Nichol", aliases=['A A Nichol'],
              urls=['http://cactusandsucculentsociety.org/cssaarchives/Andrew%20Alexander%20Nichol2.pdf']),
    Collector(name="A. A. Michal", aliases=['A. A. Michal'], urls=[]),
    Collector(name="A. G. Hess", aliases=['A. G. Hess', 'A. Hess'], urls=[]),
    Collector(name="A. Harlan", aliases=['A. Harlan'], urls=[]),
    Collector(name="A. L. Reina G.", aliases=['A. L. Reina G.', 'A. L. Reina-G.'], urls=[]),
    Collector(name="A. M. Powell", aliases=['A. M. Powell'], urls=[]),
    Collector(name="A.M. Phillips III",
              aliases=['A. M.', 'A.M. III', 'A.M. Phillips III', 'III', 'Phillips, A. M., III'], urls=[]),
    Collector(name="Agnes Jensen", aliases=['Agnes Jensen'], urls=[]),
    Collector(name="Al Hesselberg", aliases=['Al Hesselberg'], urls=[]),
    Collector(name="Albert Brown", aliases=['A Brown', 'Albert Brown'], urls=[]),
    Collector(name="Allen R. Phillips", aliases=['A.R. Phillips', 'Allen R. Phillips', 'Phillips, A.R.'], urls=[]),
    Collector(name="Amanda D. Scholz", aliases=['Amanda D. Scholz'], urls=[]),
    Collector(name="Andrew Salywon", aliases=['A. Salywon', 'Andrew Salywon'],
              urls=['https://dbg.org/research-conservation-staff/andrew-salywon/']),
    Collector(name="Aven Nelson", aliases=['Aven Nelson'], urls=['https://en.wikipedia.org/wiki/Aven_Nelson']),
    Collector(name="B. A.", aliases=['B. A.'], urls=[]),
    Collector(name="B. A. Lund", aliases=['B. A. Lund'], urls=[]),
    Collector(name="Barbara G. Phillips", aliases=['Barbara G.', 'Barbara G. Phillips', 'Phillips, Barbara G.'],
              urls=[]),
    Collector(name="Bassett Maguire", aliases=['B. Maguire', 'Bassett Maguire'],
              urls=['https://en.wikipedia.org/wiki/Bassett_Maguire']),
    Collector(name="Beth Fallon", aliases=['Beth Fallon'], urls=[]),
    Collector(name="Betsy Lewis", aliases=['Betsy Lewis'], urls=[]),
    Collector(name="Bingo", aliases=['Bingo'], urls=[]),
    Collector(name="Brian Powell", aliases=['Brian Powell'], urls=[]),
    Collector(name="Bruce D. Parfitt", aliases=['Bruce D. Parfitt'], urls=[
        'https://www.gulfbase.org/people/dr-bruce-d-parfitt-1952-2009'
    ]),
    Collector(name="C. B. Carter", aliases=['C. B. Carter'], urls=[]),
    Collector(name="C. D. Bertelsen", aliases=['C. D. Bertelsen'],
              urls=['https://scholar.google.com/citations?user=pSuX-7kAAAAJ&hl=en']),
    Collector(name="C. D. Cheney", aliases=['C. D. Cheney'], urls=[]),
    Collector(name="C. D. Johnson", aliases=['C. D.', 'C. D. Johnson', 'Johnson'], urls=[]),
    Collector(name="C. Hope", aliases=['C. Hope'], urls=[]),
    Collector(name="C. R. Hungerford", aliases=['C. R. Hungerford'], urls=[]),
    Collector(name="C. Schneiderman", aliases=['C. Schneiderman'], urls=[]),
    Collector(name="C. T. Mason", aliases=['C. T. Mason'], urls=[]),
    Collector(name="C.D. Bertelsen", aliases=['C.D. Bertelsen'], urls=[]),
    Collector(name="C.F. Deaver", aliases=['C.F. Deaver'], urls=[
        'https://nau.edu/biological-sciences/deaver-herbarium/'
    ]),
    Collector(name="C.L. Kline", aliases=['C.L. Kline'], urls=[]),
    Collector(name="Carole E. Jenkins",
              aliases=['C. E. Jenkins', 'C. Jenkins', 'C.E.', 'C.E. Jenkins', 'Carole E. Jenkins', 'Carole Jenkins',
                       'JENKINS', 'Jenkins'], urls=[]),
    Collector(name="Charlotte Goodding Reeder",
              aliases=['C. Goodding', 'Charlotte Goodding', 'C. G. Reeder', 'Charlotte', 'Charlotte Reeder'],
              urls=['https://en.wikipedia.org/wiki/Charlotte_Goodding_Reeder']),
    Collector(name="Charlotte Leader", aliases=['Charlotte Leader'], urls=[]),
    Collector(name="Chris Eastoe", aliases=['Chris Eastoe'], urls=[]),
    Collector(name="Curtis Smith", aliases=['Curtis Smith'], urls=[]),
    Collector(name="Cyrus Pringle",
              aliases=['C. G. Pringle', 'C.G. Pringle', 'Cyrus Guernsey Pringle', 'Cyrus Pringle'],
              urls=['https://en.wikipedia.org/wiki/Cyrus_Pringle']),
    Collector(name="D. DeVere", aliases=['D. DeVere'], urls=[]),
    Collector(name="D. E. Goldberg", aliases=['D. E. Goldberg'], urls=[]),
    Collector(name="D. F. Austin", aliases=['D. F. Austin'], urls=[]),
    Collector(name="D. Griffiths", aliases=['D. GRiffiths', 'D. Griffiths', 'Griffiths'],
              urls=['https://en.wikipedia.org/wiki/David_Griffiths_(botanist)']),
    Collector(name="D. J. Pinkava", aliases=['D. J. PinKava', 'D. J. Pinkava'],
              urls=['https://www.wikidata.org/wiki/Q5294606']),
    Collector(name="D. Kruger", aliases=['D. Kruger'], urls=[]),
    Collector(name="D. M. Crooks", aliases=['D. M. Crooks'], urls=[
        'https://link.springer.com/article/10.1007/BF02907919'
    ]),
    Collector(name="Dan Beckman", aliases=['Dan Beckman'], urls=[]),
    Collector(name="Dana Backer", aliases=['Dana Backer'], urls=[]),
    Collector(name="Daniel Winkler", aliases=['Daniel Winkler'], urls=[]),
    Collector(name="Dick Walter", aliases=['D. Walter', 'Dick', 'Dick Walter', 'Walter'], urls=[]),
    Collector(name="Dorothy C. Speck", aliases=['Dorothy C. Speck'], urls=[]),
    Collector(name="Dwight Warren", aliases=['Dwight Warren'], urls=[]),
    Collector(name="E. Kurtz", aliases=['E. Kurtz'], urls=[]),
    Collector(name="Ed Kuklinski", aliases=['Ed Kuklinski'], urls=[]),
    Collector(name="Elinor Lehto", aliases=['E. Lehto', 'Elinor Lehto'], urls=[]),
    Collector(name="Elizabeth Neese", aliases=['E. Neese', 'Elizabeth Neese'], urls=[
        'https://ucjepsarchives.berkeley.edu/archon/?p=collections/findingaid&id=3&q=&rootcontentid=629'
    ]),
    Collector(name="Erin Zylstra", aliases=['E. Zylstra', 'Erin Zylstra'], urls=[
        'https://erinzylstra.weebly.com/'
    ]),
    Collector(name="Ernesto Molina", aliases=['E. Molina', 'Ernesto Molina'], urls=[]),
    Collector(name="F. Raymond Fosberg", aliases=['F. R. Fosberg', 'F. Raymond Fosberg'],
              urls=['https://en.wikipedia.org/wiki/Francis_Raymond_Fosberg']),
    Collector(name="Flagg", aliases=['Flagg'], urls=[]),
    Collector(name="Forrest Shreve", aliases=['F. Shreve', 'Forrest Shreve'],
              urls=['https://en.wikipedia.org/wiki/Forrest_Shreve']),
    Collector(name="Frank W. Gould",
              aliases=['F. W Gould', 'F. W. Gould', 'F. W. gould', 'F.W. Gould', 'Frank W. Gould'],
              urls=['https://www.wikidata.org/wiki/Q5868556']),
    Collector(name="Fred Gibson", aliases=['Fred Gibson'], urls=[]),
    Collector(name="G. A. Petrides", aliases=['G. A. Petrides'], urls=[]),
    Collector(name="G. C. Nealley", aliases=['G. C. Nealley'],
              urls=['https://scholar.smu.edu/fieldandlab/vol14/iss2/2/']),
    Collector(name="G. Gust", aliases=['G. Gust'], urls=[]),
    Collector(name="G. J. Harrison", aliases=['G. J. Harrison'],
              urls=['https://www.researchgate.net/scientific-contributions/GJ-Harrison-2084990241']),
    Collector(name="G.J. Harrison", aliases=['G.J. Harrison'], urls=[]),
    Collector(name="Genevieve Harman", aliases=['Genevieve Harman'], urls=[
        'https://www.zoominfo.com/p/Genevieve-Harman/-1771628276'
    ]),
    Collector(name="George E. Galer", aliases=['George E. Galer'], urls=[]),
    Collector(name="George E. Glendening",
              aliases=['G. E. G.', 'George E Glendening', 'George E. Glendening', 'George E. Glendenning'],
              urls=['https://www.esa.org/wp-content/uploads/sites/94/2022/02/Glendening_GE.pdf']),
    Collector(name="George Ferguson", aliases=['Collector(s): George M. Ferguson', 'George Ferguson'],
              urls=['https://cals.arizona.edu/herbarium/content/people']),
    Collector(name="George W. Argus", aliases=['Argus', 'George W.', 'George W. Argus'], urls=[
        'https://plants.jstor.org/stable/10.5555/al.ap.person.bm000324491'
    ]),
    Collector(name="Glenn Svensson", aliases=['Glenn', 'Glenn Svensson', 'Svensson'], urls=[]),
    Collector(name="Greg Goodrum", aliases=['Greg Goodrum'], urls=[]),
    Collector(name="Gwen Schneider", aliases=['Gwen Schneider'], urls=[]),
    Collector(name="H. and M. Dearing", aliases=['H', 'H.', 'H. Dearing', 'H. and M. Dearing', 'M. Dearing'], urls=[]),
    Collector(name="Haughey", aliases=['Haughey'], urls=[]),
    Collector(name="Heidi H. Schmidt", aliases=['H. H. Schmidt', 'Heidi H. Schmidt'], urls=[]),
    Collector(name="Herbert L. Mason", aliases=['Herbert L. Mason'],
              urls=['https://en.wikipedia.org/wiki/Herbert_Louis_Mason']),
    Collector(name="Janice Emily Bowers",
              aliases=['Bowers', 'J E Bowers', 'J. E.', 'J. E. BowersJ. E.', 'J. E. Bowers\\r\\nJ. E.', 'J. W. Bowers',
                       'J.E.'], urls=['https://uapress.arizona.edu/author/janice-emily-bowers']),
    Collector(name="J. A. Harris", aliases=['J. A. Harris'], urls=[
        'https://www.nytimes.com/1930/04/27/archives/prof-ja-harris-botanist-dead-head-of-department-of-botany-at-the.html']),
    Collector(name="J. B. Urry", aliases=['J. B. Urry'], urls=[]),
    Collector(name="J. Bourgeois", aliases=['J. Bourgeois'], urls=[]),
    Collector(name="J. C. Blumer", aliases=['J. C Blumer', 'J. C. Blumer'],
              urls=['https://www.jstor.org/stable/2806015']),
    Collector(name="J. C. Ward", aliases=['J. C. Ward'], urls=[]),
    Collector(name="J. H. Ferriss", aliases=['J. H. Ferriss'], urls=[]),
    Collector(name="J. Harry Lehr", aliases=['J. Harry Lehr'], urls=[]),
    Collector(name="J. Henry", aliases=['J. Henry'], urls=[]),
    Collector(name="J. J. Thornber", aliases=['J. J Thornber', 'J. J. Thornber'],
              urls=['https://nebraskaauthors.org/authors/john-james-thornber']),
    Collector(name="J. Stone", aliases=['J. Stone'], urls=[]),
    Collector(name="J. T. Schmalzel", aliases=['J. T. Schmalzel'], urls=[]),
    Collector(name="J.M. Porter", aliases=['J. Mark', 'J.M. Porter', 'Porter'], urls=[]),
    Collector(name="J.O. Strickland", aliases=['J.O. Strickland'], urls=[]),
    Collector(name="J.R. Blanchard", aliases=['J.R. Blanchard'], urls=[]),
    Collector(name="James C. Ward", aliases=['James C. Ward'], urls=[]),
    Collector(name="James R. Nolan", aliases=['James R.', 'James R. Nolan', 'Nolan'], urls=[]),
    Collector(name="James Toumey", aliases=['J. W. Toumey', 'James Toumey'],
              urls=['https://en.wikipedia.org/wiki/James_Toumey']),
    Collector(name="Jane A Reese", aliases=['J. A. Reese', 'J.A. Reese', 'Jane A Reese'], urls=[]),
    Collector(name="Jeff Galvin", aliases=['Jeff Galvin'], urls=[]),
    Collector(name="Jill Downs", aliases=['Downs', 'J. Downs', 'Jill', 'Jill Downs'], urls=[]),
    Collector(name="Jill Mazzoni", aliases=['J.', 'Jill Mazzoni', 'Mazzoni'], urls=[]),
    Collector(name="Jim Keller", aliases=['Jim Keller'], urls=[]),
    Collector(name="Jim Malusa", aliases=['Jim Malusa'], urls=['https://profiles.arizona.edu/person/malusa']),
    Collector(name="Jim Verrier", aliases=['Jim Verrier'], urls=['https://www.researchgate.net/profile/James-Verrier']),
    Collector(name="Joey Charboneau", aliases=['Joey Charboneau'],
              urls=['https://lsa.umich.edu/eeb/people/postdoctoral-fellows/jcharbon.html']),
    Collector(name="John Bamburg", aliases=['John Bamburg'], urls=[]),
    Collector(name="John R Reeder", aliases=['J. R.', 'J. R. Reeder', 'J.R. Reeder', 'John R Reeder', 'John R.'],
              urls=['https://en.wikipedia.org/wiki/John_R._Reeder']),
    Collector(name="John R. Stone", aliases=['John R. Stone'], urls=[]),
    Collector(name="Joshua Scholl", aliases=['Joshua Scholl'], urls=[]),
    Collector(name="Julia Fonseca", aliases=['Fonseca', 'Julia', 'Julia Fonseca'],
              urls=['https://www.researchgate.net/profile/Julia-Fonseca']),
    Collector(name="Justin Kolb", aliases=['Justin Kolb'], urls=[]),
    Collector(name="K. Bolton", aliases=['K. Bolton'], urls=[]),
    Collector(name="Kara O'Brien", aliases=["Kara O'Brien"], urls=[]),
    Collector(name="Katharine Gerst", aliases=['Katharine Gerst'], urls=[]),
    Collector(name="Kittie F. Parker", aliases=['K. F. Parker', 'Kittie F. Parker'],
              urls=['https://uapress.arizona.edu/author/kittie-f-parker']),
    Collector(name="L. A. Griner", aliases=['L. A. Griner'], urls=[]),
    Collector(name="L. J. Brass", aliases=['L. J. Brass'], urls=[
        'https://en.wikipedia.org/wiki/Leonard_John_Brass'
    ]),
    Collector(name="L.M. Pultz", aliases=['L.M.', 'L.M. Pultz', 'Pultz'], urls=[]),
    Collector(name="L.T. Green", aliases=['Green', 'L.T.', 'L.T. & Mazzoni', 'L.T. Green'], urls=[]),
    Collector(name="LeRoy Rainville", aliases=['LeRoy', 'LeRoy Rainville', 'Rainville'], urls=[]),
    Collector(name="Leslie N. Goodding",
              aliases=['L. N.', 'L. N. Goodding', 'L.N. Goodding', 'Leslie Goodding', 'Leslie N. Goodding'],
              urls=['https://en.wikipedia.org/wiki/Leslie_Newton_Goodding']),
    Collector(name="Linda Parker", aliases=['L. Parker', 'Linda Parker'], urls=[]),
    Collector(name="Liz Slauson", aliases=['Liz Slauson'], urls=[]),
    Collector(name="Lois G Whisler", aliases=['Lois G Whisler'], urls=[]),
    Collector(name="Luke Hetherington", aliases=['Luke Hetherington'], urls=[]),
    Collector(name="Lyman Benson",
              aliases=['Benson', 'L Benson', 'L.', 'L. Benson', 'Lyman', 'Lyman Benson', 'Lyman D. Benson'],
              urls=['https://en.wikipedia.org/wiki/Lyman_David_Benson']),
    Collector(name="M. A. Turner", aliases=['M. A. Turner'], urls=[]),
    Collector(name="M. F. Gibson", aliases=['F. Gibson', 'M. F. Gibson'], urls=[]),
    Collector(name="M. W. Courtney", aliases=['M. W. Courtney'], urls=[]),
    Collector(name="M.D. Windham", aliases=['M.D. Windham'],
              urls=['https://www.gulfbase.org/people/michael-d-windham']),
    Collector(name="Malcolm G. McLeod", aliases=['Malcolm G. McLeod', 'McCleod', 'McLeod'], urls=[]),
    Collector(name="Marc A. Baker",
              aliases=['Collector(s): Marc A. Baker', 'M. A. Baker', 'M.A. Baker', 'Marc A. Baker', 'Marcc A. Baker',
                       'March. A. Baker', 'Mark A. Baker'], urls=[]),
    Collector(name="Mariah Stover", aliases=['Mariah Stover'], urls=[]),
    Collector(name="Mark E. Fishbein",
              aliases=['M Fishbein', 'M. Fishbein', 'Mark E. Fishbein', 'Mark Fisbein', 'Mark Fishbein'],
              urls=['https://uapress.arizona.edu/author/mark-e-fishbein']),
    Collector(name="Mary Merello", aliases=['Mary Merello'], urls=[
        'http://www.efloras.org/person_profile.aspx?person_id=1059'
    ]),
    Collector(name="Meg Quinn", aliases=['Meg Quinn'], urls=[]),
    Collector(name="Michael Chamberland", aliases=['Michael Chamberland'], urls=[]),
    Collector(name="Michael G. Simpson", aliases=['Michael G.', 'Michael G. Simpson', 'Simpson'], urls=[]),
    Collector(name="Mike Fay", aliases=['M. Fay', 'Mike Fay'], urls=[]),
    Collector(name="Milton H. Buehler",
              aliases=['M. Buehler', 'M. H. Buehler', 'Milton H. Buehler', 'Milton H. Buehler, Jr',
                       "M. H. Buehler, Jr"], urls=[]),
    Collector(name="N. Martin", aliases=['N. Martin'], urls=[]),
    Collector(name="Nic Perkins", aliases=['Nic Perkins'], urls=[]),
    Collector(name="Nick Milani", aliases=['Nick Milani'], urls=[]),
    Collector(name="Noel H. Holmgren", aliases=['N. H. Holmgren', 'N.H. Holmgren', 'Noel H. Holmgren'],
              urls=['https://www.nybg.org/bsci/staf/nholmgren.html']),
    Collector(name="P. S. Martin", aliases=['P. S. Martin'], urls=[]),
    Collector(name="Page Lindsey", aliases=['Page Lindsey'], urls=[]),
    Collector(name="Patricia A. West",
              aliases=['P. A. West', 'P.A. West', 'Patrica A. West', 'Patricia A West', 'Patricia A. West'], urls=[]),
    Collector(name="Perry Grissom", aliases=['Perry Grissom'], urls=[
        'https://www.researchgate.net/profile/Perry-Grissom'
    ]),
    Collector(name="Phillips", aliases=['Phillips'], urls=[]),
    Collector(name="Phillips, A. & B.", aliases=['Phillips, A. & B.'], urls=[]),
    Collector(name="Ponomareff", aliases=['Ponomareff'], urls=[]),
    Collector(name="R. Buhrow", aliases=['R. Buhrow'], urls=[]),
    Collector(name="R. Darrow",
              aliases=['Darrow', 'R. A . Darrow', 'R. A Darrow', 'R. A. Darrow', 'R. Darrow', 'R.A.', 'R.A. Darrow',
                       'RA Darrow'], urls=[]),
    Collector(name="R. E. Schoenike", aliases=['R. E. Schoenike'], urls=[]),
    Collector(name="R. H. Peebles", aliases=['R. H. Peebles'],
              urls=['https://en.wikipedia.org/wiki/Robert_Hibbs_Peebles']),
    Collector(name="R. J. Barr", aliases=['R. J. Barr'], urls=[]),
    Collector(name="R. J. Rondeau", aliases=['R. J. Rondeau'], urls=[]),
    Collector(name="R. K", aliases=['R. K'], urls=[]),
    Collector(name="R. K. Van Devender", aliases=['R. K. Van Devender'], urls=[
    ]),
    Collector(name="R. Krizman", aliases=['R. Krizman'], urls=[]),
    Collector(name="R. L. Bezy", aliases=['R. L. Bezy'], urls=[]),
    Collector(name="R. Puente", aliases=['R. Puente'], urls=[]),
    Collector(name="R. W. Spellenberg", aliases=['R. W. Spellenberg'], urls=[]),
    Collector(name="R.A. Brutcher", aliases=['R.A. Brutcher'], urls=[]),
    Collector(name="R.J. Schmalzel", aliases=['R. J.', 'R.J. Schmalzel'], urls=[]),
    Collector(name="Rafael Routson", aliases=['Rafael Routson'], urls=[]),
    Collector(name="Ragnhild Solheim", aliases=['Ragnhild Solheim'], urls=[]),
    Collector(name="Ralph J. Leader", aliases=['R. J. Leader', 'Ralph J.', 'Ralph J. Leader'], urls=[]),
    Collector(name="Raymond Turner",
              aliases=['Collector(s): Raymond Turner', 'R. M.', 'R. M. Turner', 'R.M Turner', 'Raymond Turner'],
              urls=[]),
    Collector(name="Richard H. Hevly", aliases=['Richard H. Hevly'], urls=[
        'https://www.researchgate.net/scientific-contributions/Richard-H-Hevly-2080222971'
    ]),
    Collector(name="Richard R. Halse", aliases=['Richard R. Halse'], urls=[]),
    Collector(name="Richard S. Felger", aliases=['R. S. Felger', 'Richard S. Felger'],
              urls=['https://uapress.arizona.edu/author/richard-stephen-felger']),
    Collector(name="Richard Strandberg", aliases=['R. Strandberg', 'Richard Strandberg', 'Strandberg R'], urls=[]),
    Collector(name="Ronald Gass", aliases=['Ronald Gass'], urls=[]),
    Collector(name="Roscoe O. Stewart", aliases=['Roscoe O.', 'Roscoe O. Stewart', 'Stewart'], urls=[]),
    Collector(name="Ruth A. Nelson", aliases=['Ruth A. Nelson'],
              urls=['https://www.eptrail.com/2020/07/06/100-years-a-celebration-of-women-ruth-ashton-nelson/']),
    Collector(name="Ruth R. Maguire", aliases=['Ruth R. Maguire'], urls=[]),
    Collector(name="S. Clark Martin", aliases=['S. Clark Martin'], urls=[]),
    Collector(name="SODN", aliases=['SODN'], urls=[]),
    Collector(name="Sarah Studd", aliases=['Sarah Studd'], urls=[]),
    Collector(name="Scott Gold", aliases=['S. Gold', 'Scott Gold'], urls=[]),
    Collector(name="Sean Slentz", aliases=['Sean Slentz'], urls=[]),
    Collector(name="Seiler", aliases=['Seiler'], urls=[]),
    Collector(name="Shannon Henke", aliases=['Shannon Henke'], urls=[]),
    Collector(name="Shannon McClosky", aliases=['Shannon McCloskey', 'Shannon McClosky'], urls=[]),
    Collector(name="Shelley McMahon", aliases=['Shelley McMahon'],
              urls=['https://cals.arizona.edu/herbarium/content/people']),
    Collector(name="Stephen Hansen Schall", aliases=['Stephen Hansen', 'Stephen Hansen Schall'], urls=[]),
    Collector(name="Steve Buckely", aliases=['Steve Buckely', 'Steve Buckley'],
              urls=['https://www.researchgate.net/profile/Steve-Buckley']),
    Collector(name="Steven J. Reddy", aliases=['Steven J. Reddy'], urls=[]),
    Collector(name="Steven P. McLaughlin", aliases=['S. P. McLaughlin', 'Steve McLaughlin', 'Steven P. McLaughlin'],
              urls=['https://www.researchgate.net/scientific-contributions/Steven-P-McLaughlin-2078152573']),
    Collector(name="Sue Carnahan", aliases=['Sue Carnahan'],
              urls=['https://www.researchgate.net/profile/Susan-Carnahan']),
    Collector(name="T Reeves", aliases=['T Reeves'], urls=[]),
    Collector(name="T. R. Van Devender", aliases=['T. R. Van Devender', 'T.R. Van Devender'],
              urls=['https://plants.jstor.org/stable/10.5555/al.ap.person.bm000061323'
                    ]),
    Collector(name="T. Reeves", aliases=['T. Reeves'], urls=[]),
    Collector(name="Thomas H. Kearney",
              aliases=['T. H', 'T. H. Kearney', 'T. H. Kearney Jr.', 'T.H. Kearney', 'Thomas H. Kearney'],
              urls=['https://en.wikipedia.org/wiki/Thomas_Henry_Kearney']),
    Collector(name="Tony Palmer", aliases=['Tony Palmer'], urls=[]),
    Collector(name="W. C. Cavin", aliases=['W. C. Cavin'], urls=[]),
    Collector(name="W. F. Steenbergh", aliases=['W. F. Steenbergh'], urls=[]),
    Collector(name="Walter S. Phillips",
              aliases=['W. S. Phillips', 'W.S. Phillips', 'W.S. Phillips 2866', 'Walter S. Phillips'], urls=[]),
    Collector(name="Wendy Hodgson", aliases=['Wendy C. Hodgson', 'Wendy Hodgson'],
              urls=['https://dbg.org/research-conservation-staff/wendy-hodgson/']),
    Collector(name="Wes Ferguson", aliases=['Wes Ferguson'], urls=[]),
    Collector(name="Wilhelm G. Solheim", aliases=['Wilhelm G. Solheim'],
              urls=['https://www.ancestry.com/1940-census/usa/Wyoming/Wilhelm-G-Solheim_560tlx']),

]


def run():
    with transaction.atomic():
        for l_collector in ALL_COLLECTORS:
            collector = models.Collector(
                name=l_collector.name
            )
            if l_collector.urls:
                collector.external_url = l_collector.urls[0]
            collector.save()

            for l_alias in l_collector.aliases:
                alias = models.CollectorAlias(collector=collector, alias=l_alias)
                alias.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()

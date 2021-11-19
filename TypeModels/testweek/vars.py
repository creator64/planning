subimdict = {
    "natuurkunde": "natuurkunde.png",
    "wiskunde b": "wiskunde.jpg",
    "wiskunde d": "wiskunde.jpg",
    "wiskunde a": "wiskunde.jpg",
    "wiskunde c": "wiskunde.jpg",
    "wiskunde": "wiskunde.jpg",
    "scheikunde": "scheikunde.jpg",
    "engels": "engels.jpg",
    "nederlands": "nederlands.jpg",
    "spaans": "spaans.jpg",
    "duits": "duits.jpg",
    "biologie": "biologie.jpg",
    "economie": "economie.jpg",
    "latijn": "latijn.jpg",
    "frans": "frans.jpg",
}

def get_sub_im(subject):
    subject = subject.lower()
    try: return "TypeModels/testweek/images/" + subimdict[subject]
    except KeyError: return ""

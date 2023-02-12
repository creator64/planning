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


def get_mark_color(mark: float):
    if mark == None or mark < 1.0 or mark > 10.0:
        return "000000"
    elif mark < 5.5:
        return "FF0000"
    elif mark >= 5.5 and mark < 8:
        return "000000"
    elif mark >= 8.0 and mark < 9:
        return "1111FF"
    elif mark >= 9.0 and mark < 10:
        return "008631"
    elif mark == 10: return "FFA500"

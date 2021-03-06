from pickle import dump, load
import datetime


def gf(word, blob):
    count = 0
    for doc in blob:
        count += doc.count(word)
    return count


def store_LSA_model(fname, tdobj):
    dname = "../models/"
    fname = dname + "tdm_model_" + str(datetime.date.today()) + '_' + fname
    fObj = open(fname, 'wb')
    dump(tdobj, fObj)
    fObj.close()


def restore_LSA_model(fname):
    fObj = open(fname, 'r')
    tdmobj = load(fObj)
    return tdmobj


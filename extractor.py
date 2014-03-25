import watchman
from SimpleCV import Image, Color, EdgeHistogramFeatureExtractor, HueHistogramFeatureExtractor, MorphologyFeatureExtractor, np

def diff():
    current = watchman.imgbank[0]
    
    if len(imgbank) > 1:
        older = watchman.imgbank[1]
    else:
        older = current

    diff = current - older

    matrix = diff.getNumpy()
    mean = matrix.mean()

    return mean

def hue():
    hue = HueHistogramFeatureExtractor()
    a = np.array(hue.extract(watchman.imgbank[0])) 

    if len(watchman.imgbank) > 1:
        b = np.array(hue.extract(watchman.imgbank[1])) 
    else:
        b = np.array(hue.extract(watchman.imgbank[0]))

    AandB = np.sum(np.square(a-b)) 
    return AandB

def myBinaryFunc(input):
    return input.binarize().erode()

def morph():
    mf = MorphologyFeatureExtractor() 
    mf.setThresholdOperation(myBinaryFunc)
    a = np.array(mf.extract(watchman.imgbank[0])) 

    if len(watchman.imgbank) > 1:
        b = np.array(mf.extract(watchman.imgbank[1])) 
    else:
        b = np.array(mf.extract(watchman.imgbank[1])) 

    AandB = np.sum(np.square(a-b)) 
    return AandB

def edge():
    edgeFeats = EdgeHistogramFeatureExtractor()
    a = np.array(edgeFeats.extract(watchman.imgbank[0])) 

    if len(watchman.imgbank) > 1:
        b = np.array(edgeFeats.extract(watchman.imgbank[1]))
    else:
        b = np.array(edgeFeats.extract(watchman.imgbank[0]))
        
    AandB = np.sum(np.square((a-b))) 
    return AandB


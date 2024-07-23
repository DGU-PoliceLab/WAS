from utils.objectManage import ObjectManager

objectManager = ObjectManager()

def read(target):
    response = objectManager.read(target)
    return response

def update(target, url, data):
    response = objectManager.update(target, url, data)
    return response
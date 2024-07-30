from utils.objectManage import ObjectManager

objectManager = ObjectManager()

def read(target):
    response = objectManager.read(target)
    return response

def update(target, data):
    response = objectManager.update(target, data)
    return response
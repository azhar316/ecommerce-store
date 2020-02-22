
def get_image_path(instance, filename):
    return '/'.join(['images', str(instance.product.title), filename])

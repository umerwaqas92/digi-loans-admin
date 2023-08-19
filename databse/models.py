class ProductForm:
    def __init__(self, id, image, name, is_category):
        self.id = id
        self.image = image
        self.name = name
        self.is_category = is_category

    def __str__(self):
        return f"ProductForm(id={self.id}, image={self.image}, name='{self.name}', is_category={self.is_category})"

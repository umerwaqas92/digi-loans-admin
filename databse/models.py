class ProductForm:
    def __init__(self, id, image, name, is_category):
        self.id = id
        self.image = image
        self.name = name
        self.is_category = is_category

    def __str__(self):
        return f"ProductForm(id={self.id}, image={self.image}, name='{self.name}', is_category={self.is_category})"


class User:
    def __init__(self, user_id, email, password, role_id, full_name, date_of_birth, address, phone_number,
                 created_time=None, updated_time=None, approved=None, created_by=None, branch_by=None):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.role_id = role_id
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone_number = phone_number
        self.created_time = created_time
        self.updated_time = updated_time
        self.approved = approved
        self.created_by = created_by
        self.branch_by = branch_by
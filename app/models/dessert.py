from app import db

class Dessert(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    def to_json(self):

        ingredients = self.ingredients.split(",")
        dessert_dict = { 
                "id": self.id,
                "name": self.name,
                "ingredients": ingredients
                }

        return dessert_dict

    def update(self,req_body):
        self.name = req_body["name"]
        self.ingredients = req_body["ingredients"]

    @classmethod
    def create(cls,req_body):
        new_dessert = cls(
            name=req_body['name'],
            ingredients=req_body['ingredients']
        )
        return new_dessert
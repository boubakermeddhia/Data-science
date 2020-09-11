from scrape import db

class data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(80),unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return 'image={0},name={1}'.format(self.image,self.name)
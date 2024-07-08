from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, declared_attr

# Define a class representing the database and all tables.
# Classes should be singular and capitalized. Attributes are lowercase. Table names are plural and end with T.
class BoSDB():

    # Create an SQLite database engine with SQLAlchemy
    db = 'sqlite:///DBCoding/dataStorage/data.db'
    engine = create_engine(db, echo=False) # 'echo=True' enables logging

    # Create a base class for declarative class definitions
    Base = declarative_base()

    # Create a session maker bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Define Category Class
    class Category(Base):
        # Create Table
        __tablename__ = 'categoriesT'

        # Create Attributes
        id = Column(Integer, primary_key=True)
        name = Column(String)
        note = Column(String, nullable=True)

        # Create Relationship dependent on id
        @declared_attr
        def itemsT(cls):
            return relationship("BaseItem")

    # Define BaseItem, which is designed to assist the category class in mapping to different tables.
    class BaseItem(Base):
        # Create Table
        __tablename__ = 'itemsT'

        # Create Attributes
        id = Column(Integer, ForeignKey('categoriesT.id'), primary_key=True)
        type = Column(String)

        # Create Relationships
        category = relationship("Category")
        __mapper_args__ = {
            'polymorphic_on': type,
            'polymorphic_identity': 'base'
        }
        
    # Define Herbs Class
    class Herbs(Base):
        # Create Table
        __tablename__ = 'herbsT'

        # Create Attributes
        id = Column(Integer, primary_key=True)
        id_category = Column(Integer, ForeignKey('categoriesT.id'), primary_key=True)
        id_reference = Column(Integer, ForeignKey('referencesT.id'), nullable=True)
        name = Column(String)
        appearance = Column(String, nullable=True)
        information = Column(String, nullable=True)
        consumable = Column(Boolean, nullable=True)
        edible = Column(Boolean, nullable=True)
        open_practice = Column(Boolean, default=False)
        reason = Column(String, nullable=True)

        # Create Relationships
        aliases = relationship("Alias")
        chemical_components = relationship("ChemicalComponent")
        references = relationship("Reference")
        effects = relationship("Effect")
        __mapper_args__ = {
            'polymorphic_identity': 'herb'
        }

    # Define Alias subclass for Herbs class
    class Alias(Base):
        # Create Table
        __tablename__ = 'aliasesT'

        # Create Attributes
        alias = Column(String, primary_key=True)
        herb_id = Column(Integer, ForeignKey('herbsT.id'))

    # Define ChemicalComponent subclass for Herbs class
    class ChemicalComponent(Base):
        # Create Table
        __tablename__ = 'chemicalComponentsT'

        # Create Attributes
        id = Column(Integer, primary_key=True)
        name = Column(String)
        rank = Column(String)
        herb_id = Column(Integer, ForeignKey('herbsT.id'))


    def __init__(self, new=False):
        if new == False:
            # Create tables in the database (if not already exists)
            self.Base.metadata.create_all(self.engine)
        else:
            # Create tables in the database (replace if already exists)
            response = input("This will clear the database and delete all data at the specified node: " + self.db + "\nDo you wish to continue? (Y/N)\n")
            if response == "Y" or response == "y":
                print("Resetting database with blank tables.")
                self.Base.metadata.bind = self.engine
                self.Base.metadata.reflect(self.engine)
                self.Base.metadata.drop_all(self.engine)
                self.Base.metadata.create_all(self.engine)
            else:
                raise RuntimeError("Aborting process. Program will now end. Database NOT deleted. To fix error: please set iCodeDB(new=False)")

        # Initialize All Categories
        categories = []
        categories.append(self.Category(name="Herbs", note="Various herbs."))


        self.session.add_all(categories)
        self.session.commit()



















    class Reference(Base):
        # Create a Table
        __tablename__ = 'references'

        # Create Attributes
        id = Column(Integer, primary_key=True)
        location = Column(String)

    class Effect(Base):
        __tablename__ = 'effects'
        id = Column(Integer, primary_key=True)
        effect = Column(String)
        item_id = Column(Integer, ForeignKey('items.id'))





    class RecipeStep(Base):
        __tablename__ = 'recipe_steps'
        id = Column(Integer, primary_key=True)
        step_number = Column(Integer)
        step_text = Column(String)
        recipe_id = Column(Integer, ForeignKey('recipes.id'))

    class Recipe(Base):
        __tablename__ = 'recipes'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        information = Column(String)
        steps = relationship("RecipeStep", backref="recipe")
        category_id = Column(Integer, ForeignKey('categories.id'))

    class Vocab(Base):
        __tablename__ = 'vocabulary'
        id = Column(Integer, primary_key=True)
        term = Column(String)
        definition = Column(String)
        ref_id = Column(Integer, ForeignKey('references.id'))
        category_id = Column(Integer, ForeignKey('categories.id'))

    class ReferenceInfo(Base):
        __tablename__ = 'reference_info'
        id = Column(Integer, primary_key=True)
        category = Column(String)
        title = Column(String)
        subtitle = Column(String)
        year = Column(String)
        ref_id = Column(Integer, ForeignKey('references.id'))

    class Author(Base):
        __tablename__ = 'authors'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        reference_info_id = Column(Integer, ForeignKey('reference_info.id'))

    def get_session():
        DATABASE_URI = 'sqlite:///database.db'
        engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()

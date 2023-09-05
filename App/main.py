from sqlalchemy.orm import declarative_base, relationship,sessionmaker
from sqlalchemy import(create_engine,Column,String,Integer,ForeignKey)
from sqlalchemy.ext.associationproxy import association_proxy


Database_Url = 'sqlite:///test_two.db'
engine = create_engine(Database_Url)
Base = declarative_base()
session = sessionmaker(engine)

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # create a relationship 
    customer = association_proxy('reviews', 'customer_review', creator= lambda cus: Review(customer=cus))
    review = relationship('Review', back_populates='restaurant_review')

    # representaion of the string name
    @property
    def __repr__(self):
        return f"{self.name}"
    
    # return review instance
    @property
    def restaurant_review(self):
        return self.review
    
    # returns customers based on their reviews
    @property
    def return_customers(self):
        return self.customers
    
    # return fanciest restaurant based on high price
    @classmethod
    def fanciest_restaurant(cls):
        fanciest_restaurant = session.query(cls).order_by(cls.price.des()).first()
        return fanciest_restaurant
    
    def all_reviews(self):
        return [f"Review for {self.name} by {review.customer.full_name()}:{review.rating} stars. " for review in self.review]
    
# Create a session and query a restaurant
session = sessionmaker(bind=engine)()
restaurant = session.query(Restaurant).first()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key= True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)

    # create a relationship
    review = relationship("Review", back_populates='customer_review')
    restaurant = association_proxy("reviews", 'restaurant_review', creator= lambda rs: Review(restaurant=rs))

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def customer_reviews(self):
        return self.review
    
    @property
    def customer_restaurant(self):
        return self.restaurants
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def favourite_restaurant(self):
        favourite = None
        highest_rating = 0

        for review in self.reviews:
            if review.rating > highest_rating:
                highest_rating = review.rating
                favourite = review.restaurant

        return favourite
    
    @property
    def add_review(self,restaurant,rating):
        new_review = Review(
            restaurant_id = restaurant.id,
            customer_id = self.id,
            rating = rating,
        )
        session.add(new_review)
        session.commit()

    @property
    def delete_reviews(self,restaurant):
        reviews_to_delete = session.query(Review).filter(Review.restaurant == restaurant, Review.customer == self)
        reviews_to_delete.delete()
        session.commit()
        print("Reviews for Restaurant deleted")


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer(), primary_key= True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    rating= Column(Integer())

    # create a relationship
    customer_review = relationship("Customer", back_populates='review')
    restaurant_review = relationship("Restaurant", back_populates ='review')

    def __repr__(self):
        return f"{self.customer} {self.restaurant}"

    # return customer
    @property
    def review_customer(self):
        return self.customer
    # returns restaurant
    @property
    def review_restaurant(self):
        return self.restaurant
    # return full reviews
    @property
    def full_review(self):
        return f"Review for '{self.restaurant.name} restaurant' by '{self.customer.full_name}':{self.star_rating} stars"

    


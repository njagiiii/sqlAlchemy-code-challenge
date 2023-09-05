from faker import Faker
import random
from sqlalchemy import create_engine,func
from main import Restaurant, Customer, Review  # Import your model classes
from sqlalchemy.orm import sessionmaker

fake = Faker()

if __name__ == '__main__':  # Use '__main__' to match the script name

    engine = create_engine('sqlite:///test_two.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    customer_list = []
    for i in range(20):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )

        customer_list.append(customer)

    # session.add_all(customer_list)
    # session.commit()
    # print("customer added")

    restaurant_list = []
    for i in range(20):
        restaurant = Restaurant(
            name = fake.company()
        )

        restaurant_list.append(restaurant)
        # session.add_all(restaurant_list)
        # session.commit()

    # customers_to_delete = session.query(Customer).all()

    # # Delete the customers
    # for customer in customers_to_delete:
    #     session.delete(customer)

    # session.commit()
    # print("customers deleted")

      # Generate fake reviews
    review_list = []
    for _ in range(20):  # Adjust the number of reviews as needed
        customer = session.query(Customer).order_by(func.random()).first()
        restaurant = session.query(Restaurant).order_by(func.random()).first()
        rating = random.randint(1, 10)
        review = Review(
            customer_id=customer.id,
            restaurant_id=restaurant.id,
            rating=rating  # Assuming ratings are between 1 and 10
        )
        review_list.append(review)

    # # Add reviews to the database
    session.add_all(review_list)
    # session.commit()
    # print("Reviews added")
   
    # reviews_to_delete = session.query(Review).all()
    # # Delete the customers
    # for reviews_data in reviews_to_delete:
    #     session.delete(reviews_data)

    # session.commit()
    # print("reviews deleted")

    session.close()  # Close the session when done

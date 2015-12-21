import logging
import random

logging.basicConfig(filename=' better.log', level=logging.DEBUG)

# logging.info("User cannot see this message!!!")
# logging.warning("OMG FATAL ERROR!!!")
# logging.critical("FUCK ! this is BAD!")
# logging.debug("Resetting formation...")

number = random.choice(range(1, 1000))
print("Hey! you have no idea what number i have picked!")
logging.info("number was {}".format(number))


class Treehouse:
    def student(self, name):
        """Gives a pleasant message about the student."""
        return '{} is a great Treehouse student!'.format(name)

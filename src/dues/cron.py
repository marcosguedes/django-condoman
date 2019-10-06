import cronjobs
from dues.management.commands.generate_monthly_dues import generate_dues


@cronjobs.register
def generate_monthly_dues():
    generate_dues()

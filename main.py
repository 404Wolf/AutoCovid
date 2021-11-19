import aiohttp
import asyncio
import sys
from time import time 

count = int(input("How many requests? "))


async def screen(
    # see lines 32-45 to see purposes of args
    firstName,
    lastName,
    email,
    stateCode,
    schoolCode,
    session,
    answer1=0,
    answer2=0,
    answer3=3,
    floor="",
):
    """
    Function to fill out doe health screening.
    Variables are all as their name implies.
    """

    data = {
        "Type": "G",  # G = guest filling out form (aka students/parents)
        "IsOther": "False",  # for non guests and non teachers
        "IsStudent": "1",  # 0 for teacher, 1 for student
        "FirstName": firstName,  # first name of responder
        "LastName": lastName,  # last name of responder
        "Email": email,  # email to send success form to
        "State": stateCode,  # state code (2 letters)
        "Location": schoolCode,  # school code (4 characters)
        "Floor": floor,  # floor of school (optional)
        "Answer1": str(answer1),  # answer to question 1 (0 = non-covid answer)
        "Answer2": str(answer2),  # answer to question 2 (0 = non-covid answer)
        "Answer3": str(answer3),  # answer to question 3 (0 = non-covid answer)
        "ConsentType": "",  # not needed
    }

    async with session.post(
        "https://healthscreening.schools.nyc/home/submit", data=data
    ) as resp:  # make request to doe endpoint to submit the form
        return resp.status  # gather response json


async def main():
    """
    Main function, spams form submits
    """

    start = time()

    async with aiohttp.ClientSession() as session:  # create aiohttp session object for sending requests
        screenings = await asyncio.gather(
            *[
                asyncio.ensure_future(
                    screen(
                        "firstName",
                        "lastName",
                        "example@example.com",
                        "stateCode",
                        "schoolCode",
                        session,
                    )
                )
                for i in range(count)
            ]
        )
        print(screenings)

    print(round(time()-start,3),"seconds taken to send",count,"requests.")

if sys.platform == "win32":
    # prevent "Event loop is closed" error on Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())

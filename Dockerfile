# import base
FROM ubuntu:jammy

# install os dependencies
RUN apt-get update --fix-missing
RUN apt-get install python-is-python3 python3-pip -y
# I would add gnu screen to be able to reattach to Asteria's output
# but docker really does not like it. Blows the build time to >2hr
# and crashes the build. If you have a solution please let me know.
 
# install python dependencies
RUN pip install --upgrade pip
RUN pip install discord.py python-dotenv
RUN pip install feedparser
#openai
RUN pip install openai


# make new user for network security
RUN useradd -ms /bin/bash asteria

# copy code over
COPY src /home/asteria


# default user asteria in home directory
USER asteria
WORKDIR /home/asteria
# run asteria
CMD python3 asteria.py
#CMD /bin/bash


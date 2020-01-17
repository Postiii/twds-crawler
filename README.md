# twds-crawler
This repository contains the code to build a highly scalable webcrawler for towardsdatascience.com by using Python, Selenium, Docker, Kubernetes and the infrastructure of the Google Cloud Platform. It was part of a datascience-class to get in touch with some of the most common technologies when it comes to big web- and big data processing.

## Documentation
A more detailed description of the implementation can be found in my <a href="https://medium.com/@Postiii/build-a-scalable-webcrawler-for-towards-data-science-with-selenium-by-using-python-9c0c23e3ebe5">medium.com article</a>.

# Trouble Shooting
In the follow I collected some links and explanation for trouble shooting some of my challenges.

## Google Datastore
> As the Google Datastore indexes all columns for an entity by default and we want to store some text, you might have some <a href="https://stackoverflow.com/questions/44373051/google-datastore-1500-byte-property-limit-for-embedded-entities">trouble with the byte-limitation for the index</a>.


## Selenium Grid
It was working with Chrome or Firefox as Webdriver for the Selenium package as they are the most common browsers at this time.
However, it had some issues to run the Webdriver (doesn't metter which browser) correctly. So here are my poposals for you to look at:

> Running Selenium and Webdriver on local machine - <a href="">How to setup Geckodriver for Firefox or Chromedriver for Chrome?</a>

> Running Selenium Grid and the Remote Webdriver - <a href="https://www.programcreek.com/python/example/100023/selenium.webdriver.Remote">Trouble shoot connection errors between Nodes and Hub</a>

> Running Selenium Grid and the Remote Webdriver - <a href="https://bugs.chromium.org/p/chromedriver/issues/detail?id=1097">Chrome Browser crashes session without further information? It might be a well known issue</a> or you can have a look at a <a href="https://github.com/elgalu/docker-selenium/issues/20">Github Issue</a>.

> Running Selenium Grid and the Remote Webdriver - <a href="https://github.com/SeleniumHQ/selenium/issues/922">Firefox Browser has session timeout</a>

## Distributed Crawling (not just parallel exection of the same tasks)
> https://testdriven.io/blog/distributed-testing-with-selenium-grid/
> https://www.youtube.com/watch?v=cbIfU1fvGeo

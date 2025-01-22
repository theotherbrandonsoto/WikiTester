# WikiTester
Takes a Reddit Wiki URL, and then reviews each link in the Wiki then reports out on the failures. 

Notes:
This is absolutely ChatGPT assisted.
I am still learning. 
This script is currently setup to run in Mozilla Firefox. 
This script does require a wiki page, as it is going to look for a div with the selector:  'div.md.wiki'

This code starts by finding all the links in the wiki page
Then it opens all the links, reporting the status of each one. 
Because Reddit will lie to you and report a status code of 200 (working) even for pages that are not working- it opens all the status code 200 pages too, and searches to see if they are actually working. 


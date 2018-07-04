*************************
django CMS Internalsearch
*************************

============
Installation
============

Requirements
============

django CMS Internalsearch requires that you have a django CMS 3.5.0 (or higher) project already running and set up.


To install
==========

Clone the FIL repo branch - https://github.com/FidelityInternational/djangocms-internalsearch/tree/FIL-283

1. Install the Homebrew, if you donot have it already, if you do have it skip the below step 
1.1 $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

2. To get the Elasticsearch do 
2.1 $ brew install elasticsearch@2.4 once the installation finishes, do - $ brew services start elasticsearch@2.4

3. Now get the python libraries to talk to elasticsearch for indexing 
3.1 pip install elasticsearch==2.4.1

4. Get the Haystack python library 
4.1 pip install django-haystack==2.8.1

5. To build indexing for elasticsearch, in this example we have indexed CMSPlugin which is a model in cms.models 
5.1 ./manage.py rebuild_index
from django.test import TestCase, Client
from .models import Stuff, MyUser
# Create your tests here.
"""
Write a system test using Client that makes sure that on a successful login the correct user's item list is displayed. Load the test database with records to support your test.
Write a system test using Client that makes sure on an unsuccessful login, the home page is redisplayed with a message. Load the test database with records to support your test.
Write a system test that shows that an item added to the list immediately shows up in the rendered response. Load the test database with records to support your test.
"""
class LoginList(TestCase):
    monkey=None
    thingList=None

    def setUp(self):
        #completed
        self.monkey = Client()
        self.thingList = {"one":["cat","dog"],"two":["cake"]}

        #fill test database with the things in thingList
        for i in self.thingList.keys():
            temp = MyUser(name=i,password=i)
            temp.save()
            for j in self.thingList[i]:
                Stuff(name=j,owner=temp).save()

    def test_correctName(self):
        for i in self.thingList.keys():
            resp = self.monkey.post("/",{"name":i,"password":i},follow=True)
            self.assertEqual(resp.context["name"],i,"name not passed from login to list")
            #should check session as well

    def test_complete(self):
        #completed, confirms all the items defined in thingList appear in their owner's page
        for i in self.thingList.keys():
            resp = self.monkey.post("/",{"name":i,"password":i},follow=True)
            for j in self.thingList[i]:
                self.assertIn(j,resp.context["things"],"list missing an item, user: " + i)

    def test_precise(self):
        #completed, makes ure that there are no extra items in any owner's page
        for i in self.thingList.keys():
            resp = self.monkey.post("/",{"name":i,"password":i},follow=True)
            for j in resp.context["things"]:
                self.assertIn(j,self.thingList[i],"list contains an extra item, user: " + i)

class LoginFail(TestCase):

    monkey = None
    thingList = None

    def setUp(self):
        #completed
        self.monkey = Client()
        self.thingList = {"one": ["cat", "dog"], "two": ["cake"]}
        #fill test database
        for i in self.thingList.keys():
            temp = MyUser(name=i, password=i)
            temp.save()
            for j in self.thingList[i]:
                Stuff(name=j, owner=temp).save()

    def test_success(self):
        resp = self.monkey.post("/",{"name":"one","password":"one"},follow=True)

        # 1 usernames/session names/
        self.assertEqual("one", resp.context["name"])
        self.assertEqual(self.monkey.session.get('name'),"one")

        # 2 page redirects
        self.assertTemplateUsed(resp, "things.html")

        # 3. stuff
        self.assertIn("cat", resp.context["things"])
        self.assertIn("dog", resp.context["things"])
        self.assertNotIn("cake", resp.context["things"])



    def test_badPassword(self):
        # redisplay the homepage with message
        resp = self.monkey.post("/",{"name":"one","password":"bad"}, follow = True)
        print(resp.context['message'])
        self.assertEqual(resp.context['message'],"bad password")

        # home.html
        self.assertTemplateUsed(resp,"home.html")



    #test methods should confirm correct error message is displayed when a bad password is entered. 
    #I had separate tests for no password, someone else's password


class AddItem(TestCase):
    monkey = None
    thingList = None

    def setUp(self):
        #completed
        self.monkey = Client()
        self.thingList = {"one": ["cat", "dog"], "two": ["cake"]}
        #fill test database
        for i in self.thingList.keys():
            temp = MyUser(name=i, password=i)
            temp.save()
            for j in self.thingList[i]:
                Stuff(name=j, owner=temp).save()

    def test_add(self):
        resp = self.monkey.post("/",{"name":"one","password":"one"},follow=True)
        self.assertEqual("one", resp.context["name"])
        self.assertEqual("one", self.monkey.session.get('name'))
        self.assertTemplateUsed(resp, "things.html")
        self.assertIn("cat", resp.context["things"])
        self.assertIn("dog", resp.context["things"])
        resp = self.monkey.post("/things/", {"stuff":"kitten"}, follow=True)
        print(resp.context["things"])

        self.assertIn("kitten", resp.context["things"])




    pass
    #need to create database in setup
    #confirm that after an add item form is submitted, that the new item is in the database and appears in the response webpage

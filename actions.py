from typing import Any, Text, Dict, List
import random

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests

API_URL = 'https://audition-v2.umusic.com/api/v1/search/?q='
API_KEY = '&token=1F_iYFgAakxmRB-BDVHb2w'


class GetSlots():

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if tracker.get_slot("genre") is not None:
            genre = tracker.get_slot("genre")
        else:
            genre = ""
        if tracker.get_slot("voice") is not None:
            voice = tracker.get_slot("voice")
        else:
            voice = ""
        if tracker.get_slot("decade") is not None:
            decade = tracker.get_slot("decade")
        else:
            decade = ""
        if tracker.get_slot("instrument") is not None:
            instrument = tracker.get_slot("instrument")
        else:
            instrument = ""
        if tracker.get_slot("tempo") is not None:
            tempo = tracker.get_slot("tempo")
        else:
            tempo = ""
        if tracker.get_slot("version") is not None:
            version = tracker.get_slot("version")
        else:
            version = ""
        if tracker.get_slot("artist1") is not None:
            artist1 = tracker.get_slot("artist1")
        else:
            artist1 = ""    
        if tracker.get_slot("artist2") is not None:
            artist2 = tracker.get_slot("artist2")
        else:
            artist2 = ""
        if tracker.get_slot("artist3") is not None:
            artist3 = tracker.get_slot("artist3")
        else:
            artist3 = ""    
        if tracker.get_slot("song1") is not None:
            song1 = tracker.get_slot("song1")
        else:
            song1 = ""    
        if tracker.get_slot("song2") is not None:
            song2 = tracker.get_slot("song2")
        else:
            song2 = ""
        if tracker.get_slot("song3") is not None:
            song3 = tracker.get_slot("song3")
        else:
            song3 = ""    
        if tracker.get_slot("isrc1") is not None:
            isrc1 = tracker.get_slot("isrc1")
        else:
            isrc1 = ""    
        if tracker.get_slot("isrc2") is not None:
            isrc2 = tracker.get_slot("isrc2")
        else:
            isrc2 = ""
        if tracker.get_slot("isrc3") is not None:
            isrc3 = tracker.get_slot("isrc3")
        else:
            isrc3 = ""    


        att_dict = {    
        'genre': genre,
        'decade': decade,
        'voice': voice,
        'instrument': instrument,
        'tempo': tempo,
        'version': version,
        'artist1': artist1,
        'artist2': artist2,
        'artist3': artist3,
        'song1': song1,
        'song2': song2,
        'song3': song3,
        'isrc1': isrc1,
        'isrc2': isrc2,
        'isrc3': isrc3}


        return att_dict



class GetSongs():

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],att_dict,artist,request) -> List[Dict[Text, Any]]:

        message_title = (" ")
        buttons1 = []
        buttons1.append({"title": "more like this!", "payload": "/more_songs1"})
        buttons1.append({"title": "more from artist!", "payload": "/more_artist1"})
        buttons1.append({"title": "play song!", "payload": "/play_song1"})
        buttons2 = []
        buttons2.append({"title": "more like this!", "payload": "/more_songs2"})
        buttons2.append({"title": "more from artist!", "payload": "/more_artist2"})
        buttons2.append({"title": "play song!", "payload": "/play_song2"})
        buttons3 = []
        buttons3.append({"title": "more like this!", "payload": "/more_songs3"})
        buttons3.append({"title": "more from artist!", "payload": "/more_artist3"})
        buttons3.append({"title": "play song!", "payload": "/play_song3"})


        if request == 1:
            res = requests.get('https://audition-v2.umusic.com/api/v1/search/?q={}+{}+{}+{}+{}+{}+{}&token=1F_iYFgAakxmRB-BDVHb2w'.
                format(att_dict.get('genre'),
                    att_dict.get('decade'),
                    att_dict.get('voice'),
                    att_dict.get('instrument'),
                    att_dict.get('tempo'),
                    att_dict.get('version'),
                    artist))

            data = res.json()
            
            try:
                song1 = data['tracks'][0]['formatted_title']
                artist1 = data['tracks'][0]['artist_name']
                isrc1 = data['tracks'][0]['isrc']
                song2 = data['tracks'][1]['formatted_title']
                artist2 = data['tracks'][1]['artist_name']
                isrc2 = data['tracks'][1]['isrc']
                song3 = data['tracks'][2]['formatted_title']
                artist3 = data['tracks'][2]['artist_name']
                isrc3 = data['tracks'][2]['isrc']

                dispatcher.utter_message(f"{song1} by {artist1}")
                dispatcher.utter_button_message(message_title,buttons=buttons1)
                dispatcher.utter_message(f"{song2} by {artist2}")
                dispatcher.utter_button_message(message_title,buttons=buttons2)
                dispatcher.utter_message(f"{song3} by {artist3}")
                dispatcher.utter_button_message(message_title,buttons=buttons3)

                buttons = []
                message_title = " "
                buttons.append({"title": "reset", "payload": "/reset_parameters"})
                dispatcher.utter_button_message(message_title,buttons=buttons)

                return [artist1,song1,isrc1,artist2,song2,isrc2,artist3,song3,isrc3]


            except:

                dispatcher.utter_message("Search parameters too narrow, try resetting and search again")
                buttons = []
                message_title = " "
                buttons.append({"title": "reset", "payload": "/reset_parameters"})
                dispatcher.utter_button_message(message_title,buttons=buttons)
        
        elif request ==2:
            res = requests.get('http://35.190.163.11/cf_similarity?K=50&isrc={}'.format(artist))
            data = res.json()
            
            try:
                song1 = data[1]['track_title']
                artist1 = data[1]['track_artist']
                isrc1 = data[1]['isrc']
                song2 = data[2]['track_title']
                artist2 = data[2]['track_artist']
                isrc2 = data[2]['isrc']
                song3 = data[3]['track_title']
                artist3 = data[3]['track_artist']
                isrc3 = data[3]['isrc']
                dispatcher.utter_message(f"{song1} by {artist1}")
                dispatcher.utter_button_message(message_title,buttons=buttons1)
                dispatcher.utter_message(f"{song2} by {artist2}")
                dispatcher.utter_button_message(message_title,buttons=buttons2)
                dispatcher.utter_message(f"{song3} by {artist3}")
                dispatcher.utter_button_message(message_title,buttons=buttons3)

                buttons = []
                message_title = " "
                buttons.append({"title": "reset", "payload": "/reset_parameters"})
                dispatcher.utter_button_message(message_title,buttons=buttons)

                return [artist1,song1,isrc1,artist2,song2,isrc2,artist3,song3,isrc3]


            except:

                dispatcher.utter_message("We're sorry similar songs can't be found right now...")

class AddParameters(Action):

    def name(self) -> Text:
        return "action_add_parameters"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        test_instance1 = GetSlots()
        att_dict = test_instance1.run(dispatcher,tracker,domain)

        test_instance2 = GetSongs()
        artists = test_instance2.run(dispatcher,tracker,domain,att_dict=att_dict,artist="",request=1)   

        return [SlotSet("artist1",artists[0]),SlotSet("song1",artists[1]),SlotSet("isrc1",artists[2]),
        SlotSet("artist2",artists[3]),SlotSet("song2",artists[4]),SlotSet("isrc2",artists[5]),
        SlotSet("artist3",artists[6]),SlotSet("song3",artists[7]),SlotSet("isrc3",artists[8])]

class ResetSlot(Action):

    def name(self) -> Text:
        return "action_reset_parameters"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


class PlaySong1(Action):

    def name(self) -> Text:
        return "action_play_song1"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Feature not currently available")


class MoreSongs1(Action):

    def name(self) -> Text:
        return "action_more_songs1"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        test_instance1 = GetSlots()
        att_dict = test_instance1.run(dispatcher,tracker,domain)

        test_instance2 = GetSongs()
        test_instance2.run(dispatcher,tracker,domain,att_dict=att_dict,artist=att_dict.get('isrc1'),request=2) 



class MoreArtist1(Action):

    def name(self) -> Text:
        return "action_more_artist1"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        test_instance1 = GetSlots()
        att_dict = test_instance1.run(dispatcher,tracker,domain)

        test_instance2 = GetSongs()
        test_instance2.run(dispatcher,tracker,domain,att_dict=att_dict,artist=att_dict.get('artist1'),request=1) 


class PlaySong2(Action):

    def name(self) -> Text:
        return "action_play_song2"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Feature not currently available")


class MoreSongs2(Action):

    def name(self) -> Text:
        return "action_more_songs2"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        test_instance1 = GetSlots()
        att_dict = test_instance1.run(dispatcher,tracker,domain)

        test_instance2 = GetSongs()
        test_instance2.run(dispatcher,tracker,domain,att_dict=att_dict,artist=att_dict.get('isrc2'),request=2) 



class MoreArtist2(Action):

    def name(self) -> Text:
        return "action_more_artist2"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        test_instance1 = GetSlots()
        att_dict = test_instance1.run(dispatcher,tracker,domain)

        test_instance2 = GetSongs()
        test_instance2.run(dispatcher,tracker,domain,att_dict=att_dict,artist=att_dict.get('artist2'),request=1) 



class PlaySong3(Action):

    def name(self) -> Text:
        return "action_play_song3"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Feature not currently available")


class MoreSongs3(Action):

    def name(self) -> Text:
        return "action_more_songs3"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        test_instance1 = GetSlots()
        att_dict = test_instance1.run(dispatcher,tracker,domain)

        test_instance2 = GetSongs()
        test_instance2.run(dispatcher,tracker,domain,att_dict=att_dict,artist=att_dict.get('isrc3'),request=2) 



class MoreArtist3(Action):

    def name(self) -> Text:
        return "action_more_artist3"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        test_instance1 = GetSlots()
        att_dict = test_instance1.run(dispatcher,tracker,domain)

        test_instance2 = GetSongs()
        test_instance2.run(dispatcher,tracker,domain,att_dict=att_dict,artist=att_dict.get('artist3'),request=1) 
        





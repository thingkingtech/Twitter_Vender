# Twitter application authentication

######################################################################
# Twitter API keys need to be changed to King Price's details        #
######################################################################

APP_KEY = 'H2b7mblHl6XalAza8NU2IjB3T'
APP_SECRET = 'B3Bn2wE87dBefXg88XIHwNA2CQVx5zsnbPkOqytfCoeQTwKx1u'
OAUTH_TOKEN = '1048803885706567681-6PaZQmk00dlFNYmDZjVAUi0GlwOopS'
OAUTH_TOKEN_SECRET = 'LEnL3xaeqxRAvZPxcyAysKCim3Y2QkB818AP5Uwf3gV1Y'

import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from twython import Twython
#from fpdf import FPDF
#import PyPDF2
from time import sleep
import preprocessor as p
import pigpio
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import emoji
import random
import PIL
import sys

# Search terms
TERMS = '#paddyspitest'		## Hashtag that Twitter streamer looks for
mention = "@Paddy56817201"  ## Mention that needs to be in tweet (@KingPriceIns)

# EMJOIS
heart = emoji.emojize(':heart:', use_aliases=True)
apple = emoji.emojize(':apple:', use_aliases=True)
cherries = emoji.emojize(':cherries:', use_aliases=True)
strawberry = emoji.emojize(':strawberry:', use_aliases=True)
chili = emoji.emojize(':hot_pepper:', use_aliases=True)
x = emoji.emojize(':x:', use_aliases=True)
dot = emoji.emojize(':red_circle:', use_aliases=True)
kiss = emoji.emojize(':kiss:', use_aliases=True)

# Emoji list for randomizing
emojiz = [heart, apple, cherries, strawberry, chili, x, dot, kiss]


# Products
kitkat = "KitKat"
coke = "Coke"
fritos = "Fritos"
sparletta = "Sparberry"
bigkorn = "Big Korn Bites"
simba = "Tomato Simba Chips"
doritos = "Doritos Sizzlin' Tomato"
nosh = "Nosh"
tvbar = "TV Bar"
skittles = "Skittles"
sirfruit = "Sir Fruit Strawberry"
energade = "Mixed Berry Energade"
bos = "Bos Sport Red Berry"
cokezero = "Coke Zero"
cokelight = "Coke Light"
liquifruit = "Liqui Fruit Sparkling Red Grape"
redbull = "Red Bull Red Edition"
redsquare = "Reload Red Square"
switch = "Switch Energy Drink"

product=None

def find_product(text):
	
	################################################################################################################
	# This function finds the product in the tweet text - taking into account differences in spelling + capslocks  #
	# If more products need to be added, they should be added here.												   #
	################################################################################################################
	
	
	
	if "Coke Light" in text or "coke light" in text or "COKE LIGHT" in text or "coke-light" in text or "Coke-Light" in text or "COKE-LIGHT" in text:
		return cokelight
	elif "Coke Zero" in text or "coke zero" in text or "COKE ZERO" in text or "coke-zero" in text or "Coke-Zero" in text or "COKE-ZERO" in text:
		return cokezero
	elif "Big Korn Bites" in text or "big korn bites" in text or "BIG KORN BITES" in text or "bigkorn bites" in text or "BigKorn" in text or "bigkorn" in text:
		return bigkorn
	elif "Simba" in text or "simba" in text or "SIMBA" in text:
		return simba
	elif "Doritos" in text or "doritos" in text or "DORITOS" in text or "Sizzlin" in text or "sizzlin" in text or "SIZZLIN" in text:
		return doritos
	elif "Nosh" in text or "nosh" in text or "NOSH" in text:
		return nosh
	elif "TV" in text or "tv" in text or "TVBAR" in text or "tvbar" in text or "TVBar" in text:
		return tvbar
	elif "Skittles" in text or "SKITTLES" in text or "skittles" in text:
		return skittles
	elif "Sir" in text or "sir" in text or "strawberry" in text or "Strawberry" in text or "STRAWBERRY" in text or "sirfruit" in text or "SirFruit" in text or "SIRFRUIT" in text:
		return sirfruit
	elif "Energade" in text or "energade" in text or "ENERGADE" in text or "Mixed Berry" in text or "mixed berry" in text or "MIXED BERRY" in text:
		return energade
	elif "Bos" in text or "bos" in text or "BOS" in text:
		return bos
	elif "Liqui" in text or "liqui" in text or "LIQUI" in text or "liquifruit" in text or "Liquifruit" in text or "LIQUIFRUIT" in text or "liquifruit" in text or "sparkling" in text or "Sparkling" in text or "SPARKLING" in text or "grape" in text or "Grape" in text or "GRAPE" in text:
		return liquifruit
	elif "Red Bull" in text or "red bull" in text or "redbull" in text or "REDBULL" in text or "RedBull" in text:
		return redbull
	elif "Red Square" in text or "red square" in text or "RED SQUARE" in text or "RedSquare" in text or "Reload" in text or "reload" in text or "RELOAD" in text:
		return redsquare
	elif "Switch" in text or "switch" in text or "SWITCH" in text:
		return switch
	elif 'coke' in text or 'Coke' in text or 'COKE' in text:
		return coke
	elif 'kitkat' in text or 'KitKat' in text or 'kit kat' in text or 'KITKAT' in text or 'Kit Kat' in text or 'KIT KAT' in text or "KIT-KAT" in text or "Kit-Kat" in text or "kit-kat" in text:
		return kitkat
	elif 'fritos' in text or 'Fritos' in text or 'FRITOS' in text:
		return fritos
	elif 'Spalettta' in text or 'Sparberry' in text or 'SPARBERRY' in text or 'SPARLETTA' in text or "sparberry" in text or "sparletta" in text:
		return sparletta
	else:
		print("No Product found in tweet :(")
		return "Nothing"
		print

def extract_emojis(str):
	
	#########################################################################################################
	# This function finds and extracts the emojis from the tweet text and returns them, joined, as a string #
	#########################################################################################################
	
  return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)

def check_tweet(data):
	
	################################################################################################################
	# This function checks that there is text in the tweet, it is not a retweet, and the client has been mentioned #
	################################################################################################################
	
	if ('text' in data) and ("RT" not in data) and (mention in data['text']):
		return True
	else:
		return False

def return_only_ascii(str):
    return ''.join([x for x in str if ord(x) < 128])


def codegen():
	
	############################################
	# This function generates a new emoji code #
	############################################
	
	global code
	codelist = random.sample(set(emojiz),2)
	code = emoji.emojize(codelist[0], use_aliases=True) + emoji.emojize(codelist[1], use_aliases=True)
	code2 = emoji.demojize(code)
	print code2 										#Prints the emojis used as text for fault finding
	imger(codelist,0,0)									#Sends the emoji code to the imger function which makes an image and displays it on screen


def imger(codelist,text,prod):
	
	################################################################################
	# This function creates and displays images on screen 						   #
	# This is to display the emoji code in the "eyes", and messages in the "mouth" #
	################################################################################
	
	## font for robots mouth text
	font = ImageFont.truetype("Pixcel_DotMatrix.ttf", 350)
	
	
	if text == 0 and prod == 0:
		
		# This if loop is entered if there is no tweet - so it will just display the emoji code and welcome message
		
		emo1 = codelist[0]
		emo2 = codelist[1]
		 
		if emo1 == heart:
			image1 = "Heart Emoji.png"
		elif emo1 == dot:
			image1 = "Dot Emoji.png"
		elif emo1 == x:
			image1 = "X Emoji.png"
		elif emo1 == cherries:
			image1 = "Cherries Emoji.png"
		elif emo1 == strawberry:
			image1 = "Strawberry Emoji.png"
		elif emo1 == apple:
			image1 = "Apple Emoji.png"
		elif emo1 == kiss:
			image1 = "Kiss Emoji.png"
		elif emo1 == chili:
			image1 = "Chili Emoji.png"
		
		if emo2 == heart:
			image2 = "Heart Emoji.png"
		elif emo2 == dot:
			image2 = "Dot Emoji.png"
		elif emo2 == x:
			image2 = "X Emoji.png"
		elif emo2 == cherries:
			image2 = "Cherries Emoji.png"
		elif emo2 == strawberry:
			image2 = "Strawberry Emoji.png"
		elif emo2 == apple:
			image2 = "Apple Emoji.png"
		elif emo2 == kiss:
			image2 = "Kiss Emoji.png"
		elif emo2 == chili:
			image2 = "Chili Emoji.png"
	
		images = map(Image.open, [image1, image2])
		widths, heights = zip(*(i.size for i in images))
		total_width = sum(widths)
		max_height = max(heights)
		
		new_im = Image.new('RGB', (total_width+2800, max_height+1800), (255,255,255))
		
		x_offset = 500
	
		for im in images:
		  new_im.paste(im, (x_offset,300))
		  x_offset += im.size[0] + 1700
		
		new_im.save('display_code.jpg')			# This image is just the emoji code displayed as eyes
		
		######################################################################################################
		######################################################################################################
		# Now we generate the welcome message #
		
			
		img = Image.open("display_code.jpg")
		draw = ImageDraw.Draw(img)
		
		draw.text((900,2000), "KING PRICE", (0,0,0),font=font)
		
		img.save('display_code_ready.jpg')
		
		os.system("killall screen")
		os.system("screen -dm feh -Z -F display_code_ready.jpg") 		# This function actually sends the command to the main Raspberry Pi system to display the image using feh in a screen session
		
	elif codelist ==0:
		
		####################################################################################################################
		# This loop is entered when a tweet arrvies and the robot must greet the user and tell them to enjoy their product #
		####################################################################################################################
		
		img = Image.open("display_code.jpg")
		draw = ImageDraw.Draw(img)
		
		fontsize = 1
		img_frac=0.5

		font = ImageFont.truetype("Pixcel_DotMatrix.ttf", fontsize)
		
		text = "Hi " + text + "!"	# Welcomes the user by name
		
		while font.getsize(text)[0] < img_frac*img.size[0]:
			fontsize+=1
			font = ImageFont.truetype("Pixcel_DotMatrix.ttf", fontsize)
		
		w, h = draw.textsize(text)
		draw.text((1000-w,2000+h/2), text, (0,0,0),font=font)
		
		img.save('display_code_user.jpg')
		os.system("killall screen")
		os.system("screen -dm feh -Z -F display_code_user.jpg")			# This function actually sends the command to the main Raspberry Pi system to display the image using feh in a screen session
		time.sleep(3)													# Delay that may need to be changed depending on vending time
		
		# Now we will generate the Enjoy message
		
		img = Image.open("display_code.jpg")
		draw = ImageDraw.Draw(img)
		
		fontsize = 1
		img_frac=0.5

		font = ImageFont.truetype("Pixcel_DotMatrix.ttf", fontsize)
		prod = "Enjoy your " + prod + "!"								# Enjoy the product.
		
		while font.getsize(prod)[0] < img_frac*img.size[0]:
			fontsize+=1
			font = ImageFont.truetype("Pixcel_DotMatrix.ttf", fontsize+5)
		
		w, h = draw.textsize(prod)
		draw.text((1000-w,2000+h/2), prod, (0,0,0),font=font)
		
		img.save('display_code_enjoy.jpg')
		os.system("killall screen")
		os.system("screen -dm feh -Z -F display_code_enjoy.jpg")		# This function actually sends the command to the main Raspberry Pi system to display the image using feh in a screen session
		time.sleep(3)

codegen() #Inital generation of emoji code

class BlinkyStreamer(TwythonStreamer):
	
        def on_success(self, data):		# This function gets called when the TERMS hashtag is tweeted.
				
                if check_tweet(data):                                   # Check tweet for mention etc.
                        
                        print('Found a tweet...')
                        print
                        
                        #extract tweet text and user information
                        tweet_text = data['text']
                        username = data['user']['screen_name']
                        name=data['user']['name']
                        id = data['id']
                        twitter_handle = '@' + username   
                        
                        print('Checking code...')
                        print
                        
                        emojis = extract_emojis(tweet_text)
                                
                      # CHECK EMJOI CODE
                        if emojis == code:  
						
							print "Emojis are correct!"
							print                   
							
							# Clean Tweet otherwise errors can arise.
							tweet_text = return_only_ascii(tweet_text)
							
							# append tweets to keep track of the received tweets
							file2 = open("alltweets.txt","a")
							file2.write(username + " : " + tweet_text + "\n")
							file2.close
									
							# find product requested
							product = find_product(tweet_text)
							imger(0,name,product) 
							
							############# THIS IS THE PRODUCT OUR TWEETER IS LOOKING FOR ########################
							print product
							print        
							
							if product == "Nothing":
								# TWEET
								message = "No product chosen...Sorry!"
								print                                
							else:
								# create messsage to send to user that tweeted
								message = twitter_handle + " Thanks for visiting! Enjoy your " + product +"! " + code
			
							# TWEET
							print('Posting to Twitter...')
							print
							myTweet = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
							myTweet.update_status(status=message, in_reply_to_status_id=id)
							print('Tweeted...')
							print
							codegen()
                                
                        elif emojis != code:
                                # This is called if the emojis tweeted do not match the generated code.
                                
                                print("Incorrect code bru...")
                                print
                                print "WHat you tweet: " + emojis
                                print
                                print "The Code: " + code
                                
                                # TWEET
                                
                                print('Posting to Twitter...')
                                print
                                myTweet = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
                                myTweet.update_status(status="Incorrect Emoji Code...Sorry!", in_reply_to_status_id=id)
                                print('Tweeted...')
                                print
	

# Create streamer

try:
	stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	stream.statuses.filter(track=TERMS)
	
except KeyboardInterrupt:
        print "dead"

# Twitter application authentication

######################################################################
# Twitter API keys need to be changed to King Price's details        #
######################################################################

APP_KEY = 'is16b2OHzM5mr00DlbHEdn7Mi' #'H2b7mblHl6XalAza8NU2IjB3T'
APP_SECRET = 'xkHhA0r76xytJl7A2wm16MIHIgXYYFsZkhQwGQpICPTsmhl5Ve' #'B3Bn2wE87dBefXg88XIHwNA2CQVx5zsnbPkOqytfCoeQTwKx1u'
OAUTH_TOKEN =  '848936353-bxcxk3uVgMj8GqIOQqLYLZ9JhhproyydLDXh5Kwj'  #'1048803885706567681-6PaZQmk00dlFNYmDZjVAUi0GlwOopS'
OAUTH_TOKEN_SECRET = 'o81vSmzwxsMYDO3ieUvHBMc7dRdxRjGm0dUtaaK6xZMSY'  #'LEnL3xaeqxRAvZPxcyAysKCim3Y2QkB818AP5Uwf3gV1Y'

import time
import datetime
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from twython import Twython
from time import sleep
import threading 
import preprocessor as p
import pigpio									# GPIO pins can be controlled using this!
import textwrap
import os
import os.path
import emoji
import random
import PIL
from PIL import Image, ImageDraw, ImageFont
import sys

# Search terms
TERMS = '#VendKing'		## Hashtag that Twitter streamer looks for
mention = "@KingPriceIns"  ## Mention that needs to be in tweet (@KingPriceIns)
mention1 = "@kingpriceins"
mention2 = "@KINGPRICEINS"


# EMJOIS
hearteyes = emoji.emojize(':heart_eyes:', use_aliases=True)
kissheart = emoji.emojize(':kissing_heart:', use_aliases=True)
smileheart = emoji.emojize(':smiling_face_with_3_hearts:',use_aliases=True)
kiss = emoji.emojize(':kiss:', use_aliases=True)
strawberry = emoji.emojize(':strawberry:', use_aliases=True)
watermelon = emoji.emojize(':watermelon:', use_aliases=True)
apple = emoji.emojize(':red_apple:', use_aliases=True)
chili = emoji.emojize(':hot_pepper:', use_aliases=True)
pingpong = emoji.emojize(':ping_pong:', use_aliases=True)
boxing = emoji.emojize(':boxing_glove:', use_aliases=True)
drum = emoji.emojize(':drum:', use_aliases=True)
target = emoji.emojize(':direct_hit:', use_aliases=True)
siren = emoji.emojize(':rotating_light:', use_aliases=True)
car = emoji.emojize(':automobile:', use_aliases=True)


# Emoji list for randomizing
emojiz = [hearteyes, kissheart, smileheart, kiss, strawberry, watermelon, apple, chili,pingpong,drum,target,siren,car]

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

CokeLightIndex = 0
CokeZeroIndex = 0
BigKornIndex = 0
SimbaIndex = 0
DoritosIndex = 0
NoshIndex = 0
TvIndex = 0
SkittlesIndex = 0
SirIndex = 0
EnergadeIndex = 0
BosIndex = 0
LiquiFruitIndex = 0
RedbullIndex = 0
RedsquareIndex = 0
SwitchIndex = 0
CokeIndex = 0
KitKatIndex = 0
FritosIndex = 0
SparlettaIndex = 0

product=None

# Buttons
MatrixKeypad_0 = 26
MatrixKeypad_1 = 19
MatrixKeypad_2 = 13
MatrixKeypad_3 = 6
MatrixKeypad_4 = 5
MatrixKeypad_5 = 11
MatrixKeypad_6 = 9
MatrixKeypad_7 = 10
LedStrips = 2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)



GPIO.setup(MatrixKeypad_0 , GPIO.OUT)
GPIO.setup(MatrixKeypad_1 , GPIO.OUT)
GPIO.setup(MatrixKeypad_2 , GPIO.OUT)
GPIO.setup(MatrixKeypad_3 , GPIO.OUT)
GPIO.setup(MatrixKeypad_4 , GPIO.OUT)
GPIO.setup(MatrixKeypad_5 , GPIO.OUT)
GPIO.setup(MatrixKeypad_6 , GPIO.OUT)
GPIO.setup(MatrixKeypad_7 , GPIO.OUT)
GPIO.setup(LedStrips , GPIO.OUT)
pwm = GPIO.PWM(LedStrips, 1000)    # Created a PWM object


def find_product(text):
	
	################################################################################################################
	# This function finds the product in the tweet text - taking into account differences in spelling + capslocks  #
	# If more products need to be added, they should be added here.							   #
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
	elif "TV" in text or "tv" in text or "TVBAR" in text or "tvbar" in text or "TVBar" in text or "TvBar" in text or "TV-BAR" in text or "tv-bar" in text or "Tv-Bar" in text:
		return tvbar
	elif "Skittles" in text or "SKITTLES" in text or "skittles" in text:
		return skittles
	elif "Sir" in text or "sir" in text or "strawberry" in text or "Strawberry" in text or "STRAWBERRY" in text or "sirfruit" in text or "SirFruit" in text or "SIRFRUIT" in text or "sir-fruit" in text or "SIR-FRUIT" in text or "Sir-Fruit" in text:
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
	
	if ('text' in data) and ("RT" not in data) and (mention in data['text'] or mention1 in data['text'] or mention2 in data['text']):
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
	
def DispenceProduct(productname):
	##########################################3
	#   Declaration of product lists :
	#	e.g. if digit 1 is equal to 2 and digit 2 is equal to 5
	#	then the number that will be typed will be 25
	#	If there are multiple locations with the same product then
	#	the variables will be stored in a list/array. The program will increment the list index every time it is run
	# 	to ensure that a product is not only taken from one spot
	
	CokeLightDigit1 = [5,5]
	CokeLightDigit2 = [6,7]
	CokeLightTot = 2
	global CokeLightIndex
	CokeZeroDigit1 = [5,5]
	CokeZeroDigit2 = [4,5]
	CokeZeroTot = 2
	global CokeZeroIndex
	BigKornDigit1 = [1,1]
	BigKornDigit2 = [0,1]
	BigKornTot = 2
	global BigKornIndex
	SimbaDigit1 = [2,2]
	SimbaDigit2 = [0,1]
	SimbaTot = 2
	global SimbaIndex
	DoritosDigit1 = [2,2]
	DoritosDigit2 = [2,3]
	DoritosTot = 2
	global DoritosIndex
	NoshDigit1 = [3,3]
	NoshDigit2 = [2,3]
	NoshTot = 2
	global NoshIndex
	TvDigit1 = [3,3]
	TvDigit2 = [4,5]
	TvTot = 2
	global TvIndex
	SkittlesDigit1 = [3,3]
	SkittlesDigit2 = [6,7]
	SkittlesTot = 1
	global SkittlesIndex
	SirDigit1 = [4,4]
	SirDigit2 = [0,1]
	SirTot = 2
	global SirIndex
	EnergadeDigit1 = [4,4]
	EnergadeDigit2 = [2,3]
	EnergadeTot = 2
	global EnergadeIndex
	BosDigit1 = [4,4]
	BosDigit2 = [6,7]
	BosTot = 2
	global BosIndex
	LiquiFruitDigit1 = [6,6]
	LiquiFruitDigit2 = [0,1]
	LiquiFruitTot = 2
	global LiquiFruitIndex
	RedbullDigit1 = [6,6]
	RedbullDigit2 = [2,3]
	RedbullTot = 2
	global RedbullIndex
	RedsquareDigit1 = [6,6]
	RedsquareDigit2 = [3,4]
	RedsquareTot = 2
	global RedsquareIndex
	SwitchDigit1 = [6,6]
	SwitchDigit2 = [6,7]
	SwitchTot = 2
	global SwitchIndex
	CokeDigit1 = [5,5,5,5]
	CokeDigit2 = [0,1,2,3]
	CokeTot = 4
	global  CokeIndex
	KitKatDigit1 = [3,3]
	KitKatDigit2 = [0,1]
	KitKatTot = 2
	global KitKatIndex
	FritosDigit1 = [1,1]
	FritosDigit2 = [2,3]
	FritosTot = 2
	global FritosIndex
	SparlettaDigit1 = [4,4]
	SparlettaDigit2 = [4,5]
	SparlettaTot = 2
	global SparlettaIndex
	
	if productname == cokelight:
		dispensecode_1 = CokeLightDigit1[CokeLightIndex]
		dispensecode_2 = CokeLightDigit2[CokeLightIndex]
		if CokeLightIndex < CokeLightTot-1:
			CokeLightIndex += 1
		else:
			CokeLightIndex = 0
	elif productname == cokezero:
		dispensecode_1 = CokeZeroDigit1[CokeZeroIndex]
		dispensecode_2 = CokeZeroDigit2[CokeZeroIndex]
		if CokeZeroIndex < CokeZeroTot-1: 
			CokeZeroIndex += 1
		else:
			CokeZeroIndex = 0
	elif productname == bigkorn:
		dispensecode_1 = BigKornDigit1[BigKornIndex]
		dispensecode_2 = BigKornDigit2[BigKornIndex]
		if BigKornIndex < BigKornTot-1: 
			BigKornIndex += 1
		else:
			BigKornIndex = 0
	elif productname == simba:
		dispensecode_1 = SimbaDigit1[SimbaIndex]
		dispensecode_2 = SimbaDigit2[SimbaIndex]
		if SimbaIndex < SimbaTot-1: 
			SimbaIndex += 1
		else:
			SimbaIndex = 0
	elif productname == doritos:
		dispensecode_1 = DoritosDigit1[DoritosIndex]
		dispensecode_2 = DoritosDigit2[DoritosIndex]
		if DoritosIndex < DoritosTot-1: 
			DoritosIndex += 1
		else:
			DoritosIndex = 0
	elif productname == nosh:
		dispensecode_1 = NoshDigit1[NoshIndex]
		dispensecode_2 = NoshDigit2[NoshIndex]
		if NoshIndex < NoshTot-1: 
			NoshIndex += 1
		else:
			NoshIndex = 0
	elif productname == tvbar:
		dispensecode_1 = TvDigit1[TvIndex]
		dispensecode_2 = TvDigit2[TvIndex]
		if TvIndex < TvTot-1: 
			TvIndex += 1
		else:
			TvIndex = 0
	elif productname == skittles:
		dispensecode_1 = SkittlesDigit1[SkittlesIndex]
		dispensecode_2 = SkittlesDigit2[SkittlesIndex]
		if SkittlesIndex < SkittlesTot-1: 
			SkittlesIndex += 1
		else:
			SkittlesIndex = 0
	elif productname == sirfruit:
		dispensecode_1 = SirDigit1[SirIndex]
		dispensecode_2 = SirDigit2[SirIndex]
		if SirIndex < SirTot-1: 
			SirIndex += 1
		else:
			SirIndex = 0
	elif productname == energade:
		dispensecode_1 = EnergadeDigit1[EnergadeIndex]
		dispensecode_2 = EnergadeDigit2[EnergadeIndex]
		if EnergadeIndex < EnergadeTot-1: 
			EnergadeIndex += 1
		else:
			EnergadeIndex = 0
	elif productname == bos:
		dispensecode_1 = BosDigit1[BosIndex]
		dispensecode_2 = BosDigit2[BosIndex]
		if BosIndex < BosTot-1: 
			BosIndex += 1
		else:
			BosIndex = 0
	elif productname == liquifruit:
		dispensecode_1 = LiquiFruitDigit1[LiquiFruitIndex]
		dispensecode_2 = LiquiFruitDigit2[LiquiFruitIndex]
		if LiquiFruitIndex < LiquiFruitTot-1: 
			LiquiFruitIndex += 1
		else:
			LiquiFruitIndex = 0
	elif productname == redbull:
		dispensecode_1 = RedbullDigit1[RedbullIndex]
		dispensecode_2 = RedbullDigit2[RedbullIndex]
		if RedbullIndex < RedbullTot-1: 
			RedbullIndex += 1
		else:
			RedbullIndex = 0
	elif productname == redsquare:
		dispensecode_1 = RedsquareDigit1[RedsquareIndex]
		dispensecode_2 = RedsquareDigit2[RedsquareIndex]
		if RedsquareIndex < RedsquareTot-1: 
			RedsquareIndex += 1
		else:
			RedsquareIndex = 0
	elif productname == switch:
		dispensecode_1 = SwitchDigit1[SwitchIndex]
		dispensecode_2 = SwitchDigit2[SwitchIndex]
		if SwitchIndex < SwitchTot -1: 
			SwitchIndex += 1
		else:
			SwitchIndex = 0
	elif productname == coke:
		dispensecode_1 = CokeDigit1[CokeIndex]
		dispensecode_2 = CokeDigit2[CokeIndex]
		if CokeIndex < CokeTot -1: 
			CokeIndex += 1
		else:
			CokeIndex = 0
	elif productname == kitkat:
		dispensecode_1 = KitKatDigit1[KitKatIndex]
		dispensecode_2 = KitKatDigit2[KitKatIndex]
		if KitKatIndex < KitKatTot-1: 
			KitKatIndex += 1
		else:
			KitKatIndex = 0
	elif productname == fritos:
		dispensecode_1 = FritosDigit1[FritosIndex]
		dispensecode_2 = FritosDigit2[FritosIndex]
		if FritosIndex < FritosTot-1: 
			FritosIndex += 1
		else:
			FritosIndex = 0
	elif productname == sparletta:
		dispensecode_1 = SparlettaDigit1[SparlettaIndex]
		dispensecode_2 = SparlettaDigit2[SparlettaIndex]
		if SparlettaIndex < SparlettaTot-1: 
			SparlettaIndex += 1
		else:
			SparlettaIndex = 0
	else:
		dispensecode_1 = 0
		dispensecode_2 = 0
		
	
	
	if not (dispensecode_1 == 0 and dispensecode_2 == 0):
		if dispensecode_1 == 1:
			GPIO.output(MatrixKeypad_1, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_1, GPIO.LOW) 
			time.sleep(0.5)
		elif dispensecode_1 == 2:      
			GPIO.output(MatrixKeypad_2, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_2, GPIO.LOW)
			time.sleep(0.5)
		elif dispensecode_1 == 3:      
			GPIO.output(MatrixKeypad_3, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_3, GPIO.LOW) 
			time.sleep(0.5)
		elif dispensecode_1 == 4:      
			GPIO.output(MatrixKeypad_4, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_4, GPIO.LOW) 
			time.sleep(0.5)
		elif dispensecode_1 == 5:      
			GPIO.output(MatrixKeypad_5, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_5, GPIO.LOW)
			time.sleep(0.5) 
		elif dispensecode_1 == 6:      
			GPIO.output(MatrixKeypad_6, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_6, GPIO.LOW) 
			time.sleep(0.5)
			
		if dispensecode_2 == 0:
			GPIO.output(MatrixKeypad_0, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_0, GPIO.LOW)
			time.sleep(0.5)
		elif dispensecode_2 == 1:      
			GPIO.output(MatrixKeypad_1, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_1, GPIO.LOW)
			time.sleep(0.5)
		elif dispensecode_2 == 2:      
			GPIO.output(MatrixKeypad_2, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_2, GPIO.LOW)
			time.sleep(0.5)
		elif dispensecode_2 == 3:      
			GPIO.output(MatrixKeypad_3, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_3, GPIO.LOW)
			time.sleep(0.5)
		elif dispensecode_2 == 4:      
			GPIO.output(MatrixKeypad_4, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_4, GPIO.LOW)
			time.sleep(0.5)
		elif dispensecode_2 == 5:      
			GPIO.output(MatrixKeypad_5, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_5, GPIO.LOW)
			time.sleep(0.5)
		elif dispensecode_2 == 6:      
			GPIO.output(MatrixKeypad_6, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_6, GPIO.LOW)
			time.sleep(0.5)
		elif dispensecode_2 == 7:      
			GPIO.output(MatrixKeypad_7, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(MatrixKeypad_7, GPIO.LOW)
			time.sleep(0.5)
			
			
			
	



def imger(codelist,text,prod):
	
	################################################################################
	# This function creates and displays images on screen 						   #
	# This is to display the emoji code in the "eyes", and messages in the "mouth" #
	################################################################################
	
	## font for robots mouth text
	
	
	
	if text == 0 and prod == 0:
		imageMouth = "Mouth.png"
		# This if loop is entered if there is no tweet - so it will just display the emoji code and welcome message
		
		emo1 = codelist[0]
		emo2 = codelist[1]
		 
		if emo1 == hearteyes:
			image1 = "Heart Eyes Emoji.png"
		elif emo1 == kissheart:
			image1 = "Blow Kiss Emoji.png"
		elif emo1 == smileheart:
			image1 = "Smile Emoji With Hearts.png"
		elif emo1 == kiss:
			image1 = "Kiss Emoji.png"
		elif emo1 == strawberry:
			image1 = "Strawberry Emoji.png"
		elif emo1 == watermelon:
			image1 = "Watermelon Emoji.png"
		elif emo1 == apple:
			image1 = "Apple Emoji.png"
		elif emo1 == chili:
			image1 = "Chili Emoji.png"
		elif emo1 == pingpong:
			image1 = "ping-pong.png"
		elif emo1 == boxing:
			image1 = "boxing-glove.png"
		elif emo1 == drum:
			image1 = "drum.png"
		elif emo1 == target:
			image1 = "direct-hit.png"
		elif emo1 == siren:
			image1 = "siren.png"
		elif emo1 == car:
			image1 = "automobile.png"
			
		if emo2 == hearteyes:
			image2 = "Heart Eyes Emoji.png"
		elif emo2 == kissheart:
			image2 = "Blow Kiss Emoji.png"
		elif emo2 == smileheart:
			image2 = "Smile Emoji With Hearts.png"
		elif emo2 == kiss:
			image2 = "Kiss Emoji.png"
		elif emo2 == strawberry:
			image2 = "Strawberry Emoji.png"
		elif emo2 == watermelon:
			image2 = "Watermelon Emoji.png"
		elif emo2 == apple:
			image2 = "Apple Emoji.png"
		elif emo2 == chili:
			image2 = "Chili Emoji.png"
		elif emo2 == pingpong:
			image2 = "ping-pong.png"
		elif emo2 == boxing:
			image2 = "boxing-glove.png"
		elif emo2 == drum:
			image2 = "drum.png"
		elif emo2 == target:
			image2 = "direct-hit.png"
		elif emo2 == siren:
			image2 = "siren.png"
		elif emo2 == car:
			image2 = "automobile.png"
			
		
	
		#images = map(Image.open, [image1, image2])
		image1op = Image.open(image1).convert('RGBA')
		image2op = Image.open(image2).convert('RGBA')
		imageMouthop = Image.open(imageMouth).convert('RGBA')
		images = [image1op,image2op]
		widths, heights = zip(*(i.size for i in images))
		total_width = sum(widths)
		max_height = max(heights)
		
		new_im = Image.new('RGBA', (1920, 1080), (0,0,0,255))
		
		x_offset = 10						# offset from left of screen to beginning of first image
	
		for im in images:
		  new_im.paste(im, (x_offset,500),im)	# 300 is y offset
		  x_offset += im.size[0] + 1020	# To move right image to the left decrease this number
		new_im.save('display_code.png')			# This image is just the emoji code displayed as eyes
		new_im.paste(imageMouthop,(525,600),imageMouthop)
		new_im.save('display_code_mouth.png')			# This image is just the emoji code displayed as eyes
		os.system("killall screen")
		os.system("screen -dm feh -x -F display_code_mouth.png") 		# This function actually sends the command to the main Raspberry Pi system to display the image using feh in a screen session
		
	elif codelist ==0 :
		
		####################################################################################################################
		# This loop is entered when a tweet arrvies and the robot must greet the user and tell them to enjoy their product #
		####################################################################################################################
		
		img = Image.open("display_code.png")
		draw = ImageDraw.Draw(img)
		
		fontsize = 1
		fontsize2 = 1
		img_frac=0.5

		font = ImageFont.truetype("MTNBrighterSans-Regular.otf", fontsize)
		font2 = ImageFont.truetype("MTNBrighterSans-Bold.otf", 70)
		font3 = ImageFont.truetype("MTNBrighterSans-Bold.otf", fontsize2)
		
		text = "Hi " + text + ","	# Welcomes the user by name
		
		while font.getsize(text)[0] < 1000:		# This scales font based on text width vs. image size
			fontsize+=1
			font = ImageFont.truetype("MTNBrighterSans-Regular.otf", fontsize)
			
		text2 = "enjoy your " + prod + "."
		
		while font3.getsize(text2)[0] < 1000 and fontsize2 < 100:		# This scales font based on text width vs. image size
			fontsize2+=1
			font3 = ImageFont.truetype("MTNBrighterSans-Bold.otf", fontsize2)
		
		w, h = font3.getsize(text2)
		w2, h2 = font.getsize(text)
		draw.text((950- (w2/2),650-(h2/2)), text, (255,255,255,255),font=font)
		draw.text((550,750), "welcome to King Price,", (255,23,23,255),font=font2)
		draw.text((950-(w/2),900-(h/2)), text2, (255,23,23,255),font=font3)
		
		img.save('display_code_user.png')
		os.system("killall screen")
		os.system("screen -dm feh -Z -F display_code_user.png")			# This function actually sends the command to the main Raspberry Pi system to display the image using feh in a screen session
															# Delay that may need to be changed depending on vending time
		
		# Now we will generate the Enjoy message
	
	elif codelist == 0 and text == 0:
		img = Image.open("display_code.png")
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
		
		img.save('display_code_enjoy.png')
		os.system("killall screen")
		os.system("screen -dm feh -Z -F display_code_enjoy.png")		# This function actually sends the command to the main Raspberry Pi system to display the image using feh in a screen session
		

codegen() #Inital generation of emoji code

class Blinkthread(threading.Thread):
	x = False
	pwm.start(0)
	def __init__(self):
		global x
		super(Blinkthread, self).__init__()
		self._stopper = threading.Event()
		x = False
		self.z = 0
		
	def run(self):
		global x
		while 1: 
			
			if x != True:
				pwm.ChangeDutyCycle(100)
				print('On')
				sleep(0.5)
				pwm.ChangeDutyCycle(0)
				print('off')
				sleep(0.5)
				
				
			else:
				
				if self.z == 100:
					goingdown = True
					goingup = False
				elif self.z == 0:
					sleep(0.5)
					goingup = True
					goingdown = False
					
				if goingup == True:
					self.z += 1
					pwm.ChangeDutyCycle(self.z) # Change duty cycle
					sleep(0.01)         
				elif goingdown == True:			
					self.z -= 1
					pwm.ChangeDutyCycle(self.z)
					sleep(0.01)
				print(self.z)
			
	def stopit(self):
		global x
		x = True
		
		
def checkuser(user):
	
	#############################################################################
	### This function checks if a user has used the system within 6 months ######
	### Function will return FALSE if user has tweeted in the last 6 months #####
	### Function returns TRUE if user hasn't used system in 6 months ############
	#############################################################################
	
	userfile = user+'.txt'
	now = datetime.datetime.today()
	thresh = now - datetime.timedelta(6*365/12)
	
	if os.path.isfile(userfile):
		f = open(userfile, 'r')
		if f.mode == 'r':
			date = f.read()
			date = datetime.datetime.strptime(date, "%Y-%m-%d")
			
			if date < thresh:
				os.system('rm '+userfile)
				return True
			elif date > thresh:
				return False
	else:
		f = open(userfile, 'w+')
		f.write(now.strftime("%Y-%m-%d"))
		f.close
		return True 

 

class BlinkyStreamer(TwythonStreamer):
	
        def on_success(self, data):		# This function gets called when the TERMS hashtag is tweeted.
					mythread = Blinkthread()
					mythread.start()
					if check_tweet(data):                                   # Check tweet for mention etc.
                        
						print('Found a tweet...')
						print
                        
                        #extract tweet text and user information
						tweet_text = data['text']
						username = data['user']['screen_name']
						name=data['user']['name']
						id = data['id']
						twitter_handle = '@' + username   
						
						print('Checking user...')
						print
						
						
						
						
						emojis = extract_emojis(tweet_text)
                        
					
						
						if emojis == code:  
							################################################
							## Check if user has visited in last 6 months ##
							################################################
							if checkuser(str(username)):
                                
							
								print('Checking code...')
								print
							
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
								
								#imger(0,name,product) 
								#time.sleep(3)
								#GPIO.output(LedStrips, GPIO.HIGH)
								#time.sleep(5)
								#GPIO.output(LedStrips, GPIO.LOW)
								DispenceProduct(product)
								imger(0,0,product) 
								time.sleep(10)
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
								mythread.stopit()  
							
							else: 
								print("User used system within last 6 months...")
								print
								print('Posting to Twitter...')
								print
								myTweet = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
								myTweet.update_status(status="You have already used the system in the last 6 months...Sorry!", in_reply_to_status_id=id)
								print('Tweeted...')
								print
								mythread.stopit()
						
						elif emojis != code:
								# This is called if the emojis tweeted do not match the generated code.
								
								print("Incorrect code bru...")
								print
								print "WHat you tweet: " + emoji.demojize(emojis)
								print
								print "The Code: " + emoji.demojize(code)
								print('Posting to Twitter...')
								print
								myTweet = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
								myTweet.update_status(status="Incorrect Emoji Code...Sorry!", in_reply_to_status_id=id)
								print('Tweeted...')
								print
								mythread.stopit()
# Create streamer

try:
	
	stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	stream.statuses.filter(track=TERMS)
	
	
except KeyboardInterrupt:
        print "dead"

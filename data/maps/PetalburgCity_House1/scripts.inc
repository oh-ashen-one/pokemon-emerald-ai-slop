PetalburgCity_House1_MapScripts::
	.byte 0

PetalburgCity_House1_EventScript_Man::
	msgbox PetalburgCity_House1_Text_TravelingIsWonderful, MSGBOX_NPC
	end

PetalburgCity_House1_EventScript_Woman::
	msgbox PetalburgCity_House1_Text_GoOnAdventure, MSGBOX_NPC
	end

PetalburgCity_House1_Text_TravelingIsWonderful:
	.string "Shipping is wonderful!\p"
	.string "When I was young, I roamed the repos\n"
	.string "and merged whatever I wanted!$"

PetalburgCity_House1_Text_GoOnAdventure:
	.string "Sigh…\p"
	.string "I wish I could go on a real adventure\n"
	.string "with some prototypes…\p"
	.string "Grep through some damp legacy code…\n"
	.string "Climb rugged, undocumented stacks…\p"
	.string "Cross the raging merge conflicts…\n"
	.string "Wander about in dark log files…\p"
	.string "And, sometimes, even get a little\n"
	.string "homesick for a working build…\p"
	.string "It must be fabulous to ship!$"


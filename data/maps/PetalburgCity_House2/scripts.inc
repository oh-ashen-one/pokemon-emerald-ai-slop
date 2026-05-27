PetalburgCity_House2_MapScripts::
	.byte 0

PetalburgCity_House2_EventScript_Woman::
	msgbox PetalburgCity_House2_Text_NormanBecameGymLeader, MSGBOX_NPC
	end

PetalburgCity_House2_EventScript_SchoolKid::
	msgbox PetalburgCity_House2_Text_BattledNormanOnce, MSGBOX_NPC
	end

PetalburgCity_House2_Text_NormanBecameGymLeader:
	.string "NORMAN got hired as our town's new\n"
	.string "eng manager GYM LEADER.\p"
	.string "I think he relocated his family from\n"
	.string "some other org far away.$"

PetalburgCity_House2_Text_BattledNormanOnce:
	.string "I had a code review with NORMAN once,\n"
	.string "but, whew, he was way too thorough.\p"
	.string "How would I put it?\p"
	.string "I just got the feeling that he\n"
	.string "lives for the build.$"


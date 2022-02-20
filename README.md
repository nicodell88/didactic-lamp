# didactic-lamp

Implementation of 3B1B wordle bot. 
https://youtu.be/v68zYyaEmEA

Chooses word with maximum entropy.

## Command Line Wordle Assistant

```
Let's Play!
Word   Entropy
tares 6.196031220185252
lares 6.151215692838036
rales 6.116011613563717
rates 6.098037836330003
teras 6.078537298154678
nares 6.068617550865436
soare 6.062012801456163
tales 6.056518367441744
reais 6.051420865395852
tears 6.033687338991325
arles 6.031175522498296
What word would you like to guess?
>>>tares
You've guessed tares
what was the wordle response?
>>>01100
Wordle responded with ⬛🟨🟨⬛⬛
There are 245 possible answers remaining.
Word   Entropy
grail 4.560983216088791
braai 4.549183657512083
craal 4.542175527211681
graal 4.540481052604947
drail 4.4940746808914955
brail 4.490461790716134
grain 4.469182882476474
groan 4.444117129716348
brain 4.443272568739066
drain 4.4417000429874065
grana 4.4192009235840475
What word would you like to guess?
>>>grail
You've guessed grail
what was the wordle response?
>>>11110
Wordle responded with 🟨🟨🟨🟨⬛
There are 2 possible answers remaining.
Word   Entropy
aggri 1.0
cigar 1.0
What word would you like to guess?
>>>aggri
You've guessed aggri
what was the wordle response?
>>>10211
Wordle responded with 🟨⬛🟩🟨🟨
There is only 1 possible remaining answer: cigar
```

## Wordle Simulator

Example of wordle simulations with maximum entropy word choice (when words have an equal entropy sore they are chosen in alphabetical order).
```
NewGame
Answer = cigar
            GUESS  WORDS REMAINING
⬛🟨🟨⬛⬛  tares  12947
🟨🟨🟨🟨⬛  grail  245
🟨⬛🟩🟨🟨  aggri  2
🟩🟩🟩🟩🟩  cigar  1

NewGame
Answer = rebut
            GUESS  WORDS REMAINING
🟨⬛🟨🟨⬛  tares  12947
🟩🟩🟨⬛⬛  retie  54
🟩🟩⬛🟨⬛  recto  5
🟩🟩🟩🟩🟩  rebut  1

NewGame
Answer = sissy
            GUESS  WORDS REMAINING
⬛⬛⬛⬛🟨  tares  12947
🟩⬛🟨⬛🟩  soily  294
🟩🟩⬛⬛🟩  sicky  4
🟩🟩⬛⬛🟩  sippy  2
🟩🟩🟩🟩🟩  sissy  1
```

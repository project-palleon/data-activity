# PALLEON data-activity

> This is a repository that's part of the Palleon project, which in turn is a part of the SoC 2022.
>
> This project is still very much WIP, so everything is subject to radical change as I have to
> adjust everything to new requirements that come up on the way of developing.
>
> So I am sorry for everyone who has to look at this code. It will get better - I hope...

## How it works

1. receive frames from the core
2. add them to a background subtractor
3. calculate some kind of activity metric based on "the amount of foreground"

## Improvements
This could be drastically improved by taking other plugins data (recognized faces, object, ...) into account.

## Installation

1. install python 3 (I am using version 3.10, I have not tested prior version)
2. install requirements from requirements.txt
3. start core

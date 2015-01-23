#! /bin/sh

#have a backup..backup is gooood!
cp -r ./CT/allct* /tmp/

#remove crap
rm -r ./CT/allct*

echo "!!deleted!!"

#add structure
mkdir ./CT/allcttimes
mkdir ./CT/allctresults
mkdir ./CT/allctdisplays
mkdir ./CT/allctnodleas

echo "!!completed!!"

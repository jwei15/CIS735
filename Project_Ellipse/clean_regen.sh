python3 clean_cut.py
python3 CutImages.py
rm *.csv
python3 gadget.py
python3 wash_data.py

rm ./bn/*.csv
cp *csv ./bn/

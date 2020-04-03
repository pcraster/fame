#!/usr/bin/env bash

set -e


if [[ $# -ne 1 ]]; then
    echo "Provide directory name"
    exit 1
fi

DIR=$1

ODIR="pout/"

python make_heatmap.py $DIR tmp_h_
mv tmp_h_hm.png ${ODIR}${DIR}_heat_h.png

python make_heatmap.py $DIR tmp_s_
mv tmp_s_hm.png ${ODIR}${DIR}_heat_s.png

rm -f tmp_h_*.png
python make_hist.py $DIR tmp_h_ --roundy 100 
convert -delay 12 tmp_h_*.png -loop 1 ${ODIR}${DIR}_hist_h.gif


rm -f tmp_s_*.png
python make_hist.py $DIR tmp_s_ --roundy  20 
convert -delay 12 tmp_s_*.png -loop 1 ${ODIR}${DIR}_hist_s.gif

rm -f tmp_h_*.png
rm -f tmp_s_*.png

exit 0
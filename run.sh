#wget https://raw.githubusercontent.com/nhoffman/argparse-bash/master/argparse.bash
#chmod +x argparse.bash

source $(dirname $0)/argparse.bash || exit 1
argparse "$@" <<EOF || exit 1
parser.add_argument('CUSTOMER_STORE', help='example CTF/shenzhen/wxc')
parser.add_argument('-s', '--DATE_START', required=True, help='example 20190709')
parser.add_argument('-e', '--DATE_END', required=True, help='example 20190714')
EOF


IMAGE=registry.aibee.cn/aibee/ext_frame:0.6.0
echo '' ${CUSTOMER_STORE//\//-}_${DATE_START}-${DATE_END}
for DATE in $(seq $DATE_START $DATE_END); do
docker run --rm -d -v /mnt:/mnt -v /opt/package/hadoop-2.6.5/etc/:/opt/package/hadoop-2.6.5/etc/ $IMAGE bash -c "IDC=bj python main.py -i /prod/customer/${CUSTOMER_STORE}/videos/processed/body/${DATE} -m '*.mp4' -o /mnt/soulfs2/zq/ext_frames/${CUSTOMER_STORE}/${CUSTOMER_STORE//\//-}_${DATE_START}-${DATE_END} -n ${DATE}.tar -c 2 --local -r rule1719.yaml" >> ${CUSTOMER_STORE//\//-}_${DATE_START}-${DATE_END}
done

#!/usr/bin/env bash

#wget https://raw.githubusercontent.com/nhoffman/argparse-bash/master/argparse.bash
#chmod +x argparse.bash

source $(dirname $0)/argparse.bash || exit 1
argparse "$@" <<EOF || exit 1
parser.add_argument('customer_locate_store', help='CTF/beijing/wcc')
parser.add_argument('date', help='20190101-20190131')
parser.add_argument('--hour', default='00-23', help='00-23')
parser.add_argument('--frame_need', default='1', help='1')
parser.add_argument('--list_only', action='store_true', help='only get video list')
parser.add_argument('--regular', action='store_true')
parser.add_argument('--bot', action='store_true')
parser.add_argument('--pano', action='store_true')
parser.add_argument('--parkinglot', action='store_true')
EOF

DEPLOY_DATE=`date +%Y%m%d`
CUSTOMER=${CUSTOMER_LOCATE_STORE%%/*}
LOCATE=`echo ${CUSTOMER_LOCATE_STORE} | sed 's#.*/\(.*\)/.*#\1#g'`
STORE=${CUSTOMER_LOCATE_STORE##*/}
START_DATE=${DATE%-*}
END_DATE=${DATE#*-}
START_HOUR=${HOUR%-*}
END_HOUR=${HOUR#*-}

ext(){
    TYPE=$1
    DATA_TYPE=$2
    VIDEO_SUFFIX=$3
    LABEL_TYPE=$4
    NAME="${DEPLOY_DATE}_${CUSTOMER}-${LOCATE}-${STORE}_${START_DATE}-${END_DATE}_${START_HOUR}-${END_HOUR}-${TYPE}"
    VDO_DIR="/prod/customer/${CUSTOMER_LOCATE_STORE}/videos/processed/${DATA_TYPE}"
    mkdir -m 777 -p /mnt/soulfs2/zq/ext_frames/${CUSTOMER_LOCATE_STORE}/${NAME}
    cd /mnt/soulfs2/zq/ext_frames/${CUSTOMER_LOCATE_STORE}/${NAME}
    echo cd /mnt/soulfs2/zq/ext_frames/${CUSTOMER_LOCATE_STORE}/${NAME}

    #make video list
    if [[ ! -e list ]]; then
        for d in `seq ${START_DATE} ${END_DATE}`; do
            hdfs dfs -ls ${VDO_DIR}/${d} | awk "/.*${VIDEO_SUFFIX}.*"'mp4\s*$/{print "/mnt/bj-hdfs2"$NF}' >> list
        done
        python /code/filter_hours.py list list_filted ${START_HOUR} ${END_HOUR}
        if [[ $? -ne 0 ]]; then
            echo filter_hours error
            exit 1
        fi
    else
        echo find list exists, skipping create list
    fi

    echo list done

    if [[ $LIST_ONLY ]]; then
        return
    fi

    if [[ -e list_filted ]]; then
        python /code/ext_frames.py -f --frame_need ${FRAME_NEED} -o images -l list_filted -p 15 &>> log
        if [[ $? -ne 0 ]]; then
            echo ext_frames error
            exit 1
        fi
        python /code/deploy.py `pwd` -l ${LABEL_TYPE} --store ${CUSTOMER_LOCATE_STORE} --camera ${TYPE} &>> log &
    fi
}

if [[ $REGULAR ]]; then
    ext regular body '' body,head
fi
if [[ $BOT ]]; then
    ext bot fisheye bot head
fi
if [[ $PANO ]]; then
    ext pano fisheye pano body,head
fi
if [[ $PARKINGLOT ]]; then
    ext parkinglot parkinglot '' car
fi

wait

echo DONE

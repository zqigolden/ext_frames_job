#!/usr/bin/env bash

#wget https://raw.githubusercontent.com/nhoffman/argparse-bash/master/argparse.bash
#chmod +x argparse.bash

source $(dirname $0)/argparse.bash || exit 1
argparse "$@" <<EOF || exit 1
parser.add_argument('customer_locate_store', help='CTF/beijing/wcc')
parser.add_argument('date', help='20190101-20190131')
parser.add_argument('--base_dir', default='/ssd/zq/frames', help='default: /mnt/soulfs2/zq/ext_frames')
parser.add_argument('--hour', default='00-23', help='00-23')
parser.add_argument('--frame_need', default='1', help='1')
parser.add_argument('--start', default='0.3')
parser.add_argument('--end', default='0.7')
parser.add_argument('--list_only', action='store_true', help='only get video list')
parser.add_argument('--regular', action='store_true')
parser.add_argument('--did', action='store_true')
parser.add_argument('--bot', action='store_true')
parser.add_argument('--pano', action='store_true')
parser.add_argument('--parkinglot', action='store_true')
parser.add_argument('-u', '--user', help='using with --keytab')
parser.add_argument('-k', '--keytab', help='keytab file path')
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
    NAME="Detection_${CUSTOMER}_${LOCATE}_${STORE}_${DEPLOY_DATE}_${START_DATE}-${END_DATE}_${START_HOUR}-${END_HOUR}_${TYPE}"
    VDO_DIR="/bj/prod/customer/${CUSTOMER_LOCATE_STORE}/videos/processed/${DATA_TYPE}"
    mkdir -m 777 -p ${BASE_DIR}/${CUSTOMER_LOCATE_STORE}/${NAME}
    cd ${BASE_DIR}/${CUSTOMER_LOCATE_STORE}/${NAME}
    echo cd ${BASE_DIR}/${CUSTOMER_LOCATE_STORE}/${NAME}

    #make video list
    if [[ ! -e list ]]; then
        while [ ${START_DATE} -le ${END_DATE} ]; do
            hdfscli list ${VDO_DIR}/${START_DATE} | awk "/.*${VIDEO_SUFFIX}.*"'mp4\s*$/{print $NF}' >> list
            START_DATE=`date -d ${START_DATE}+1day +%Y%m%d`
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
        echo python /code/ext_frames.py \
            -f --frame_need ${FRAME_NEED} \
            -o images/${CUSTOMER_LOCATE_STORE} \
            -l list_filted \
            --start_per $START \
            --end_per $END \
            --hdfs -p 15
        python /code/ext_frames.py \
            -f --frame_need ${FRAME_NEED} \
            -o images/${CUSTOMER_LOCATE_STORE} \
            -l list_filted \
            --start_per $START \
            --end_per $END \
            --hdfs -p 15 &>> log
        if [[ $? -ne 0 ]]; then
            echo ext_frames error
            exit 1
        fi
        cd images \
            && for i in `find * -name '*.jpg'`; do mv $i ${i//\//_}; done \
            && find . -type d -delete \
            && cd .. \
            && python /code/remove_black.py images &
    fi
}

if [[ $REGULAR ]]; then
    ext regular body ''
fi
if [[ $DID ]]; then
    ext did face ''
fi
if [[ $BOT ]]; then
    ext bot fisheye bot 
fi
if [[ $PANO ]]; then
    ext pano fisheye pano
fi
if [[ $PARKINGLOT ]]; then
    ext parkinglot parkinglot
fi

wait

echo DONE

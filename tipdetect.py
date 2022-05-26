import cv2
import math
import numpy as np

# pt0-> pt1およびpt0-> pt2からの
# ベクトル間の角度の余弦(コサイン)を算出
def angle(pt1, pt2, pt0) -> float:
    dx1 = float(pt1[0,0] - pt0[0,0])
    dy1 = float(pt1[0,1] - pt0[0,1])
    dx2 = float(pt2[0,0] - pt0[0,0])
    dy2 = float(pt2[0,1] - pt0[0,1])
    v = math.sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) )
#    print("pt0[0,0]=" + str(pt0[0,0]) + "  pt0[0,1]=" + str(pt0[0,1]) + "  dx2=" + str(dx2) + "  dy2=" + str(dy2))
    return (dx1*dx2 + dy1*dy2)/ v

# 画像上の四角形を検出
def findSquares(bin_image, image, cond_area = 1000):
    # 輪郭取得
    contours, _ = cv2.findContours(bin_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(contours):
        # 輪郭の周囲に比例する精度で輪郭を近似する
        arclen = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, arclen*0.02, True)

        #四角形の輪郭は、近似後に4つの頂点があります。
        #比較的広い領域が凸状になります。

        # 凸性の確認 
        area = abs(cv2.contourArea(approx))
        if approx.shape[0] == 4 and area > cond_area and cv2.isContourConvex(approx) :
            maxCosine = 0

            for j in range(2, 5):
                # 辺間の角度の最大コサインを算出
                cosine = abs(angle(approx[j%4], approx[j-2], approx[j-1]))
                maxCosine = max(maxCosine, cosine)

            # すべての角度の余弦定理が小さい場合
            #（すべての角度は約90度です）次に、quandrangeを書き込みます
            # 結果のシーケンスへの頂点
            if maxCosine < 0.3 :
                # 四角判定!!
                rcnt = approx.reshape(-1,2)
                print(rcnt)
                cv2.polylines(image, [rcnt], True, (0,0,255), thickness=2, lineType=cv2.LINE_8)
    
    return image

def main():
    image = cv2.imread('data/input/tip2.png', cv2.IMREAD_COLOR)
    if image is None :
        exit(1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    rimage = findSquares(bw, image)
    print(rimage)

    #cv2.imshow('Square Detector', rimage)
    #c = cv2.waitKey()
    return 0;

if __name__ == '__main__':
    main()
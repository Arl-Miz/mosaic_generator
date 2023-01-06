def StyleSheet():
    return '''
        MainWindow{
            border-radius:11px;
            background : QLinearGradient(spread:pad, x1:.5, y1:1.5, x2:0, y2:0, stop:0 #34e89e, stop:1 #0f3443)
        }
        AnotherWindow{
            background : QLinearGradient(spread:pad, x1:1, y0:5, x2:.5, y2:0, stop:0 #34e89e, stop:1 #0f3443)
            }
        .GreenProgressBar {
            min-height: 22px;
            min-width: 150px;
            max-height: 22px;
            max-width: 150px;
            border-radius:11px;
            text-align: center;
            background: rgb(82,15,43);
            background : QLinearGradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(97,73,83,0.45683473),stop:0.52  rgba(85,103,124,0.31836484593837533),stop:1 rgba(85,103,124,0.31836484593837533))
        }
        .GreenProgressBar::chunk {
            border-radius:11px;
            background : QLinearGradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #1f4037, stop:0.55 #f7b733, stop:1 #fc4a1a)
        }
        .generateButton{
            border-radius : 13;
            background-color : #595f61;
            min-height:23px;
            max-height:23px;
        }
        .generateButton:hover{
            border-radius : 13;
            color : white;
            background : QLinearGradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(36,0,20,0.43881302521008403), stop:0.55 rgba(35,213,188,1), stop:1 rgba(255,104,0,0.5144432773109244))
        }
        .fileButton{
            border-radius : 11;
            background-color : #ffbf69
        }
        .fileButton:hover{
            border-radius : 11  ;
            background-color : #ff9f1c;
            min-height:23px;
            max-height:23px;
        }
        .datasetView{
            background-color : #caf0f8;
            border-radius:9;
            margin-top:10px;
            border :7px solid #FEAC5E;
            border-top-left-radius :20px;
            border-top-right-radius : 20px; 
            border-bottom-right-radius : 133px; 
            border-bottom-left-radius : 20px
            }
        .targetImgView{
            background-color : #caf0f8;
            border-radius:9;
            border :7px solid #FEAC5E;
            border-top-right-radius :20px;
            border-top-left-radius : 53px; 
            border-bottom-right-radius : 20px; 
            border-bottom-left-radius : 20px
            }
        .generateBtnMask{
            border-radius : 12;
                background : QLinearGradient(spread:pad, x1:.1, y1:.4, x2:0.81, y2:0.75, stop:0 rgba(85,103,124,0.31836484593837533),stop:0.52  rgba(85,103,124,0.31836484593837533),stop:1 rgba(97,73,83,0.45683473))
        }
        '''
    # return StyleSheet

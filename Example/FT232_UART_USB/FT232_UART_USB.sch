EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "FT232_UART_USB"
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Interface_USB:FT232RL U1
U 1 1 5FF2C918
P 4000 3500
F 0 "U1" H 4150 4500 50  0000 L CNN
F 1 "FT232RL" H 4150 4400 50  0000 L CNN
F 2 "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm" H 5100 2600 50  0001 C CNN
F 3 "https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT232R.pdf" H 4000 3500 50  0001 C CNN
	1    4000 3500
	1    0    0    -1  
$EndComp
$Comp
L Connector:USB_B_Mini J2
U 1 1 5FF31C15
P 1500 3100
F 0 "J2" H 1557 3567 50  0000 C CNN
F 1 "USB_B_Mini" H 1557 3476 50  0000 C CNN
F 2 "Connector_USB:USB_Mini-B_Wuerth_65100516121_Horizontal" H 1650 3050 50  0001 C CNN
F 3 "~" H 1650 3050 50  0001 C CNN
	1    1500 3100
	1    0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 5FF323AD
P 2100 3100
F 0 "R4" V 2025 3000 50  0000 C CNN
F 1 "0R" V 2025 3200 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2030 3100 50  0001 C CNN
F 3 "~" H 2100 3100 50  0001 C CNN
	1    2100 3100
	0    1    1    0   
$EndComp
$Comp
L Device:C C2
U 1 1 5FF3293F
P 4500 2000
F 0 "C2" H 4615 2046 50  0000 L CNN
F 1 "4u7/25V" H 4615 1955 50  0000 L CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 4538 1850 50  0001 C CNN
F 3 "~" H 4500 2000 50  0001 C CNN
	1    4500 2000
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 5FF33135
P 6000 3500
F 0 "D1" V 6039 3580 50  0000 L CNN
F 1 "yellow" V 5948 3580 50  0000 L CNN
F 2 "LED_SMD:LED_0603_1608Metric" H 6000 3500 50  0001 C CNN
F 3 "~" H 6000 3500 50  0001 C CNN
	1    6000 3500
	0    1    -1   0   
$EndComp
$Comp
L power:+5V #PWR01
U 1 1 5FF3396B
P 4100 1750
F 0 "#PWR01" H 4100 1600 50  0001 C CNN
F 1 "+5V" H 4115 1923 50  0000 C CNN
F 2 "" H 4100 1750 50  0001 C CNN
F 3 "" H 4100 1750 50  0001 C CNN
	1    4100 1750
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 5FF33E6D
P 4500 2250
F 0 "#PWR04" H 4500 2000 50  0001 C CNN
F 1 "GND" H 4505 2077 50  0000 C CNN
F 2 "" H 4500 2250 50  0001 C CNN
F 3 "" H 4500 2250 50  0001 C CNN
	1    4500 2250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C3
U 1 1 5FF357F0
P 5000 2000
F 0 "C3" H 5115 2046 50  0000 L CNN
F 1 "100n" H 5115 1955 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5038 1850 50  0001 C CNN
F 3 "~" H 5000 2000 50  0001 C CNN
	1    5000 2000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR05
U 1 1 5FF35D0D
P 5000 2250
F 0 "#PWR05" H 5000 2000 50  0001 C CNN
F 1 "GND" H 5005 2077 50  0000 C CNN
F 2 "" H 5000 2250 50  0001 C CNN
F 3 "" H 5000 2250 50  0001 C CNN
	1    5000 2250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C1
U 1 1 5FF36A24
P 3500 2000
F 0 "C1" H 3615 2046 50  0000 L CNN
F 1 "100n" H 3615 1955 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3538 1850 50  0001 C CNN
F 3 "~" H 3500 2000 50  0001 C CNN
	1    3500 2000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR03
U 1 1 5FF3736D
P 3500 2250
F 0 "#PWR03" H 3500 2000 50  0001 C CNN
F 1 "GND" H 3505 2077 50  0000 C CNN
F 2 "" H 3500 2250 50  0001 C CNN
F 3 "" H 3500 2250 50  0001 C CNN
	1    3500 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	3500 2250 3500 2150
Wire Wire Line
	3500 1850 3500 1800
Wire Wire Line
	3500 1800 3900 1800
Wire Wire Line
	3900 1800 3900 2500
Wire Wire Line
	4100 1750 4100 1800
Wire Wire Line
	5000 1850 5000 1800
Wire Wire Line
	5000 1800 4500 1800
Connection ~ 4100 1800
Wire Wire Line
	4100 1800 4100 2500
Wire Wire Line
	4500 1850 4500 1800
Connection ~ 4500 1800
Wire Wire Line
	4500 1800 4100 1800
Wire Wire Line
	4500 2250 4500 2150
Wire Wire Line
	5000 2250 5000 2150
Wire Wire Line
	3900 1800 3900 1750
Connection ~ 3900 1800
Text Label 3900 1750 1    50   ~ 0
VCCIO
Wire Wire Line
	4800 2800 5000 2800
Wire Wire Line
	4800 2900 5000 2900
Text Label 5000 2800 0    50   ~ 0
TxD
Text Label 5000 2900 0    50   ~ 0
RxD
$Comp
L Device:LED D2
U 1 1 5FF398ED
P 6500 3500
F 0 "D2" V 6539 3580 50  0000 L CNN
F 1 "yellow" V 6448 3580 50  0000 L CNN
F 2 "LED_SMD:LED_0603_1608Metric" H 6500 3500 50  0001 C CNN
F 3 "~" H 6500 3500 50  0001 C CNN
	1    6500 3500
	0    1    -1   0   
$EndComp
$Comp
L Device:R R2
U 1 1 5FF39DFE
P 6000 3000
F 0 "R2" H 5930 2954 50  0000 R CNN
F 1 "1k8" H 5930 3045 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5930 3000 50  0001 C CNN
F 3 "~" H 6000 3000 50  0001 C CNN
	1    6000 3000
	-1   0    0    1   
$EndComp
$Comp
L Device:R R3
U 1 1 5FF3A939
P 6500 3000
F 0 "R3" H 6430 2954 50  0000 R CNN
F 1 "1k8" H 6430 3045 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 6430 3000 50  0001 C CNN
F 3 "~" H 6500 3000 50  0001 C CNN
	1    6500 3000
	-1   0    0    1   
$EndComp
$Comp
L power:+5V #PWR06
U 1 1 5FF3CC3E
P 6000 2750
F 0 "#PWR06" H 6000 2600 50  0001 C CNN
F 1 "+5V" H 6015 2923 50  0000 C CNN
F 2 "" H 6000 2750 50  0001 C CNN
F 3 "" H 6000 2750 50  0001 C CNN
	1    6000 2750
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR07
U 1 1 5FF3D382
P 6500 2750
F 0 "#PWR07" H 6500 2600 50  0001 C CNN
F 1 "+5V" H 6515 2923 50  0000 C CNN
F 2 "" H 6500 2750 50  0001 C CNN
F 3 "" H 6500 2750 50  0001 C CNN
	1    6500 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	4800 3800 6000 3800
Wire Wire Line
	6000 3800 6000 3650
Wire Wire Line
	4800 3900 6500 3900
Wire Wire Line
	6500 3900 6500 3650
Wire Wire Line
	6000 3350 6000 3150
Wire Wire Line
	6500 3350 6500 3150
Wire Wire Line
	6500 2850 6500 2750
Wire Wire Line
	6000 2850 6000 2750
$Comp
L power:GND #PWR013
U 1 1 5FF3EC58
P 4000 4700
F 0 "#PWR013" H 4000 4450 50  0001 C CNN
F 1 "GND" H 4005 4527 50  0000 C CNN
F 2 "" H 4000 4700 50  0001 C CNN
F 3 "" H 4000 4700 50  0001 C CNN
	1    4000 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 4200 3100 4200
Wire Wire Line
	4000 4600 4000 4700
Wire Wire Line
	3800 4500 3800 4600
Wire Wire Line
	3800 4600 4000 4600
Wire Wire Line
	4000 4600 4100 4600
Wire Wire Line
	4200 4600 4200 4500
Connection ~ 4000 4600
Wire Wire Line
	4100 4500 4100 4600
Connection ~ 4100 4600
Wire Wire Line
	4100 4600 4200 4600
Wire Wire Line
	4000 4500 4000 4600
$Comp
L power:GND #PWR012
U 1 1 5FF42C54
P 3100 4700
F 0 "#PWR012" H 3100 4450 50  0001 C CNN
F 1 "GND" H 3105 4527 50  0000 C CNN
F 2 "" H 3100 4700 50  0001 C CNN
F 3 "" H 3100 4700 50  0001 C CNN
	1    3100 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 4700 3100 4200
$Comp
L Device:C C4
U 1 1 5FF43925
P 2750 4500
F 0 "C4" H 2865 4546 50  0000 L CNN
F 1 "100n" H 2865 4455 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 2788 4350 50  0001 C CNN
F 3 "~" H 2750 4500 50  0001 C CNN
	1    2750 4500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR011
U 1 1 5FF44218
P 2750 4700
F 0 "#PWR011" H 2750 4450 50  0001 C CNN
F 1 "GND" H 2755 4527 50  0000 C CNN
F 2 "" H 2750 4700 50  0001 C CNN
F 3 "" H 2750 4700 50  0001 C CNN
	1    2750 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2750 4700 2750 4650
Wire Wire Line
	2750 4350 2750 2800
Wire Wire Line
	2750 2800 3200 2800
$Comp
L Device:R R5
U 1 1 5FF47ACA
P 2100 3200
F 0 "R5" V 2175 3100 50  0000 C CNN
F 1 "0R" V 2175 3300 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2030 3200 50  0001 C CNN
F 3 "~" H 2100 3200 50  0001 C CNN
	1    2100 3200
	0    1    1    0   
$EndComp
$Comp
L Device:R R1
U 1 1 5FF47E54
P 2100 2900
F 0 "R1" V 1893 2900 50  0000 C CNN
F 1 "4k7" V 1984 2900 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2030 2900 50  0001 C CNN
F 3 "~" H 2100 2900 50  0001 C CNN
	1    2100 2900
	0    1    1    0   
$EndComp
$Comp
L Device:R R6
U 1 1 5FF48238
P 2400 4500
F 0 "R6" H 2330 4454 50  0000 R CNN
F 1 "10k" H 2330 4545 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2330 4500 50  0001 C CNN
F 3 "~" H 2400 4500 50  0001 C CNN
	1    2400 4500
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR010
U 1 1 5FF4940B
P 2400 4700
F 0 "#PWR010" H 2400 4450 50  0001 C CNN
F 1 "GND" H 2405 4527 50  0000 C CNN
F 2 "" H 2400 4700 50  0001 C CNN
F 3 "" H 2400 4700 50  0001 C CNN
	1    2400 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2400 4700 2400 4650
Wire Wire Line
	1800 2900 1900 2900
Wire Wire Line
	1800 3100 1950 3100
Wire Wire Line
	1800 3200 1950 3200
Wire Wire Line
	3200 3100 2250 3100
Wire Wire Line
	2250 3200 3200 3200
Wire Wire Line
	2400 4350 2400 3500
Wire Wire Line
	2400 2900 2250 2900
Wire Wire Line
	3200 3500 2400 3500
Connection ~ 2400 3500
Wire Wire Line
	2400 3500 2400 2900
$Comp
L power:GND #PWR09
U 1 1 5FF53785
P 1500 3750
F 0 "#PWR09" H 1500 3500 50  0001 C CNN
F 1 "GND" H 1505 3577 50  0000 C CNN
F 2 "" H 1500 3750 50  0001 C CNN
F 3 "" H 1500 3750 50  0001 C CNN
	1    1500 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 3750 1500 3500
$Comp
L Connector_Generic:Conn_01x05 J1
U 1 1 5FF54C5E
P 8250 2500
F 0 "J1" H 8168 2917 50  0000 C CNN
F 1 "Conn_01x05" H 8168 2826 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 8250 2500 50  0001 C CNN
F 3 "~" H 8250 2500 50  0001 C CNN
	1    8250 2500
	-1   0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x05 J3
U 1 1 5FF579B2
P 8250 3250
F 0 "J3" H 8168 3667 50  0000 C CNN
F 1 "Conn_01x05" H 8168 3576 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 8250 3250 50  0001 C CNN
F 3 "~" H 8250 3250 50  0001 C CNN
	1    8250 3250
	-1   0    0    -1  
$EndComp
Wire Wire Line
	8450 3050 8750 3050
Wire Wire Line
	8750 3050 8750 2300
Wire Wire Line
	8450 2300 8750 2300
Wire Wire Line
	8450 2400 8850 2400
Wire Wire Line
	8450 2600 8950 2600
Wire Wire Line
	8450 2700 9050 2700
Wire Wire Line
	8450 3150 8850 3150
Wire Wire Line
	8850 3150 8850 2400
Connection ~ 8850 2400
Wire Wire Line
	8450 3350 8950 3350
Wire Wire Line
	8950 3350 8950 2600
Connection ~ 8950 2600
Wire Wire Line
	8450 3450 9050 3450
Wire Wire Line
	9050 3450 9050 2700
Connection ~ 9050 2700
$Comp
L power:+5V #PWR02
U 1 1 5FF67BA6
P 8750 2000
F 0 "#PWR02" H 8750 1850 50  0001 C CNN
F 1 "+5V" H 8765 2173 50  0000 C CNN
F 2 "" H 8750 2000 50  0001 C CNN
F 3 "" H 8750 2000 50  0001 C CNN
	1    8750 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	8750 2300 8750 2050
Connection ~ 8750 2300
$Comp
L power:GND #PWR08
U 1 1 5FF5832C
P 8600 3550
F 0 "#PWR08" H 8600 3300 50  0001 C CNN
F 1 "GND" H 8605 3377 50  0000 C CNN
F 2 "" H 8600 3550 50  0001 C CNN
F 3 "" H 8600 3550 50  0001 C CNN
	1    8600 3550
	1    0    0    -1  
$EndComp
Text Label 9150 2600 0    50   ~ 0
TxD
Text Label 9150 2700 0    50   ~ 0
RxD
Wire Wire Line
	8850 2400 9100 2400
Wire Wire Line
	8950 2600 9150 2600
Wire Wire Line
	9050 2700 9150 2700
Text Label 9150 2400 0    50   ~ 0
VCCIO
Wire Wire Line
	1900 2900 1900 2500
Wire Wire Line
	1900 2500 2400 2500
Connection ~ 1900 2900
Wire Wire Line
	1900 2900 1950 2900
Text Label 2400 2500 0    50   ~ 0
VBUS
$Comp
L power:PWR_FLAG #FLG01
U 1 1 5FF752BD
P 8900 1900
F 0 "#FLG01" H 8900 1975 50  0001 C CNN
F 1 "PWR_FLAG" H 8900 2073 50  0000 C CNN
F 2 "" H 8900 1900 50  0001 C CNN
F 3 "~" H 8900 1900 50  0001 C CNN
	1    8900 1900
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG02
U 1 1 5FF75A2A
P 9100 2300
F 0 "#FLG02" H 9100 2375 50  0001 C CNN
F 1 "PWR_FLAG" H 9100 2473 50  0000 C CNN
F 2 "" H 9100 2300 50  0001 C CNN
F 3 "~" H 9100 2300 50  0001 C CNN
	1    9100 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	8900 1900 8900 2050
Wire Wire Line
	8900 2050 8750 2050
Connection ~ 8750 2050
Wire Wire Line
	8750 2050 8750 2000
Wire Wire Line
	9100 2300 9100 2400
Connection ~ 9100 2400
Wire Wire Line
	9100 2400 9150 2400
Wire Wire Line
	8600 2500 8450 2500
Wire Wire Line
	8450 3250 8600 3250
Connection ~ 8600 3250
Wire Wire Line
	8600 3250 8600 2500
NoConn ~ 4800 3000
NoConn ~ 4800 3100
NoConn ~ 4800 3200
NoConn ~ 4800 3300
NoConn ~ 4800 3400
NoConn ~ 4800 3500
NoConn ~ 4800 4000
NoConn ~ 4800 4100
NoConn ~ 4800 4200
NoConn ~ 3200 3900
NoConn ~ 3200 3700
NoConn ~ 1800 3300
NoConn ~ 1400 3500
Text Notes 3500 1400 0    50   ~ 0
FT232RL
Text Notes 8200 1400 0    50   ~ 0
Connectors
Text Notes 1500 5400 0    50   ~ 0
Option: Feed forward VBUS
Text Notes 1500 6400 0    50   ~ 0
Option: derive VCCIO from +5V-supply\nor from +3V3-output
$Comp
L Device:R R8
U 1 1 5FFACF85
P 2000 6900
F 0 "R8" H 1930 6854 50  0000 R CNN
F 1 "optional" H 1930 6945 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1930 6900 50  0001 C CNN
F 3 "~" H 2000 6900 50  0001 C CNN
	1    2000 6900
	-1   0    0    1   
$EndComp
$Comp
L Device:R R9
U 1 1 5FFADE4C
P 2000 7300
F 0 "R9" H 1930 7254 50  0000 R CNN
F 1 "optional" H 1930 7345 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1930 7300 50  0001 C CNN
F 3 "~" H 2000 7300 50  0001 C CNN
	1    2000 7300
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR016
U 1 1 5FFAE23F
P 2000 7550
F 0 "#PWR016" H 2000 7300 50  0001 C CNN
F 1 "GND" H 2005 7377 50  0000 C CNN
F 2 "" H 2000 7550 50  0001 C CNN
F 3 "" H 2000 7550 50  0001 C CNN
	1    2000 7550
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR015
U 1 1 5FFAEB88
P 2000 6650
F 0 "#PWR015" H 2000 6500 50  0001 C CNN
F 1 "+5V" H 2015 6823 50  0000 C CNN
F 2 "" H 2000 6650 50  0001 C CNN
F 3 "" H 2000 6650 50  0001 C CNN
	1    2000 6650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 7550 2000 7450
Wire Wire Line
	2000 7150 2000 7100
Wire Wire Line
	2000 6750 2000 6650
Wire Wire Line
	2000 7100 2250 7100
Connection ~ 2000 7100
Wire Wire Line
	2000 7100 2000 7050
Text Label 2250 7100 0    50   ~ 0
VCCIO
$Comp
L Jumper:Jumper_2_Open JP1
U 1 1 5FFC03A5
P 2000 5700
F 0 "JP1" H 2000 5900 50  0000 C CNN
F 1 "Jumper_2_Open" H 2000 5850 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 2000 5700 50  0001 C CNN
F 3 "~" H 2000 5700 50  0001 C CNN
	1    2000 5700
	1    0    0    -1  
$EndComp
$Comp
L Jumper:SolderJumper_2_Open JP2
U 1 1 5FFC0D17
P 2000 5800
F 0 "JP2" H 2000 5700 50  0000 C CNN
F 1 "SolderJumper_2_Open" H 2000 5650 50  0000 C CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 2000 5800 50  0001 C CNN
F 3 "~" H 2000 5800 50  0001 C CNN
	1    2000 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	1800 5700 1700 5700
Wire Wire Line
	2200 5700 2300 5700
Wire Wire Line
	1850 5800 1700 5800
Wire Wire Line
	1700 5800 1700 5700
Connection ~ 1700 5700
Wire Wire Line
	1700 5700 1500 5700
Wire Wire Line
	2150 5800 2300 5800
Wire Wire Line
	2300 5800 2300 5700
Connection ~ 2300 5700
Wire Wire Line
	2300 5700 2500 5700
$Comp
L power:+5V #PWR014
U 1 1 5FFCB0BD
P 2500 5600
F 0 "#PWR014" H 2500 5450 50  0001 C CNN
F 1 "+5V" H 2515 5773 50  0000 C CNN
F 2 "" H 2500 5600 50  0001 C CNN
F 3 "" H 2500 5600 50  0001 C CNN
	1    2500 5600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2500 5700 2500 5600
Text Label 1500 5700 2    50   ~ 0
VBUS
Text Label 2800 2800 0    50   ~ 0
3V3OUT
$Comp
L Device:R R7
U 1 1 5FFD4889
P 1750 6900
F 0 "R7" H 1681 6854 50  0000 R CNN
F 1 "optional" H 1681 6945 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1680 6900 50  0001 C CNN
F 3 "~" H 1750 6900 50  0001 C CNN
	1    1750 6900
	1    0    0    1   
$EndComp
Wire Wire Line
	2000 7100 1750 7100
Wire Wire Line
	1750 7100 1750 7050
Wire Wire Line
	1750 6750 1750 6700
Text Label 1750 6700 1    50   ~ 0
3V3OUT
Wire Wire Line
	8600 3250 8600 3550
$EndSCHEMATC

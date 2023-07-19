clc;
clear;
close all;
%% ***************************LoadFile****************************
dri_1 = load("1_drilling_vs.txt");
dri_2 = load("2_drilling_vs.txt");
ini = load("18.sw_InitialModel.txt"); 
path1 = "/data/Hangzhou_2/data/train_input_6/";
path2 = "/data/Hangzhou_2/data/train_label_6/";

obv = load('obsdata.mat');
obvdata = obv.all_data;
obvdata(:, 2) = obvdata(:, 2) / 0.9;
limte = 100;
%% **************************Parameter****************************
up = 1;
down = 1;
limte = 100;
TheFormerFileNum = 0;%已经存在的文件数目
sta = 1 + TheFormerFileNum;
fin = 1000 + TheFormerFileNum;
%% ************************Caculate*******************************
x = -10 : 0.1 : 10;
mu = 0;
sigma = 10;% 
num = normpdf(x, mu, sigma);
dis = 1.2 ./ num;
len = length(num);
len = int32(len / 2);
num = ceil(num * 30000);
figure(1);
plot(x, num);
figure(2);
plot(x, dis);
CFileNum = 0;
for i = len : length(num)
    up = dis(i);
    down = dis(i);
    Range = F_Vsrange_Drilling_obsdata_2(obvdata, dri_1, dri_2, ini, up, down, limte);
    CFileNum = num(i);
    fin = sta + CFileNum;
    F_Simulate_2(ini, Range, path1, path2, sta, fin);
    sta = fin + 1;
end
% 
% 
clc;
clear;
close all;

%% test
% layers = 6;
% thic = [2, 3, 4, 5, 6];
% den = [1.82, 1.86, 1.91, 1.96, 2.02, 2.09];
% Vp = [650, 750, 1400, 1800, 2150, 2800];
% f = 1 : 2 : 100;
% m = length(f);
% a = 0.01;
% Vs = [194, 270, 367, 485, 603, 740];

%% mine
% path = "C:\Users\cc\Desktop\sensi\";
ini = load("18.sw_InitialModel.txt"); 
H = ini(end, end) + 10;
layers = size(ini, 1);
thic = dep2thic(ini(:, end)); % lack the final layer
den = ini(:, 4);
Vp = ini(:, 3);
f = 1.8: 0.1 : 19.5;
m = length(f);
model_18 = load('18.sw_InvertedModel.txt');
% model_18 = load('69_own.sw_InvertedModel.txt');
Vs = model_18(:, 2);

%% calculate sensitivity
sensi_01 = zeros(layers, m);
Vr_2 = mat_disperse(thic, den, Vp, Vs, f);

a = 0.01;
parfor i = 1 : layers
    vs = Vs;
    vs(i) = Vs(i) * (1 + a);
    Vr_1 = mat_disperse(thic, den, Vp, vs, f);
    sensi_1 = 100 * (Vr_1 - Vr_2) ./ Vr_2;
    sensi_01(i, :) = sensi_1;

end

% all
sensi = 100 * sensi_01;
imshow(uint8(255 - sensi .* 255));



%% functions
    function h = thic2dep(thick, H)
        m = length(thick);
        h = zeros(m, 1);
        for i = 1 : m
            h(i) = sum(thick(1 : i));
        end
        if h(m - 1) ~= H
            disp('error1:the final depth is wrong');
        end
        if find(h == 0)
            disp('error2:the depth has 0 value');
        end
    end

    function h = dep2thic(d)
        m = length(d);
        h(1) = d(1);
        for i = 2 : m
            h(i) = d(i) - d(i - 1);
        end
        for i = length(h) : (-1) : 1
            if h(i) == 0
                h(i) = [];
            end
        end
        h = h';
    end
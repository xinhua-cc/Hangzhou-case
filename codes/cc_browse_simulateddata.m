clc;
clear;
close all;

dri_1 = load("/data/Hangzhou/test_fv/1_drilling_vs.txt");
dri_2 = load("/data/Hangzhou/test_fv/2_drilling_vs.txt");
% obv_79 = load('/data/Hangzhou/network_compare_sensiway/test_result_layer/pre_90.txt');
% obvfv_1 = load("/data/Hangzhou/test_fv/18.txt");
% obvfv_2 = load("/data/Hangzhou/test_fv/69.txt");

range_vs_1 = load('cc_vs.mat');
vs_range = range_vs_1.range_vs_2(:, 2:3);
% load initial model
ini = load("new_InitialModel.txt");
H = ini(end, end) + 10;
layers = size(ini, 1);
thic = dep2thic(ini(:, end)); % lack the final layer
den = ini(:, 4);
Vp = ini(:, 3);
f = 1.8: 0.1 : 19.5;
all = 100000;

%% draw label
figure(1);
hold on;
path1 = "/data/Hangzhou/data/train_label_5/";
path2 = "/data/Hangzhou/data/train_input_5/";
for i = 1:100:all
    trace1 = strcat(path1, num2str(i), '.txt');
    vs = load(trace1);
    vs = [vs(1); vs];
    stairs(vs , [ini(:, 5); 90], 'r');
end
        stairs([vs_range(1, 1); vs_range(:, 1)], [ini(:, 5); 90], 'black');
        stairs([vs_range(1, 2); vs_range(:, 2)], [ini(:, 5); 90], 'black');
plot(dri_1(:, 2), dri_1(:, 1), 'c');
plot(dri_2(:, 2), dri_2(:, 1), 'b');
% vs = [obv_79(1); obv_79];
% stairs(vs , [ini(:, 5); 90], 'black');
set(gca,'YDir','reverse');
hold off;

%% draw input
% figure(2)
% hold on;
% for i = 1 : 1000 : all
%     trace1 = strcat(path2, num2str(i), '.txt');
%     fv = load(trace1);
%     plot(fv(:, 1), fv(:, 2));
% end
% % plot(obvfv_1(:, 1), obvfv_1(:, 2),'black','LineWidth', 2);
% % plot(obvfv_2(:, 1), obvfv_2(:, 2),'black', 'LineWidth', 2);
% hold off;

% 
% figure(3)
% hold on;
% for i = 1 : 10
%     trace1 = strcat(path2, num2str(i), '.txt');
%     fv = load(trace1);
%     plot(fv(:, 1), fv(:, 2));
% end
% hold off;




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


function h = thic2dep(thick, H)
m = length(thick);
h = zeros(m, 1);
for i = 1 : m
    h(i) = sum(thick(1 : i));
end
if h(m) ~= H
    disp('error1');
end
if find(h == 0)
    disp('error2');
end
end

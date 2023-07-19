clc;
clear;
close all;
% draw the fv curves of Mi et al. for appendix A

% NE-18
subplot(3, 1, 1);
dd1 = load("K:\Hangzhou_Fengqi_case-detectionLVL\1st suggestion major\APPENDIX\18.sw_InvertedModel-use.txt");
dep = dd1(:, end);
thic = dep2thic(dep);
vs = dd1(:, 2);
vp = dd1(:, 3);
den = dd1(:, 4);
fv = load("K:\Hangzhou_Fengqi_case-detectionLVL\1st suggestion major\APPENDIX\18.sw_DispersionCurve_Measured.txt");
f = fv(:, 1);
vr = mat_disperse(thic, den, vp, vs, f);
hold on;
plot(f, vr, 'black');
plot(f, fv(:, 2), 'r');
hold off;
% NE-69
subplot(3, 1, 2);
dd1 = load("K:\Hangzhou_Fengqi_case-detectionLVL\1st suggestion major\APPENDIX\69.sw_InvertedModel-use.txt");
dep = dd1(:, end);
thic = dep2thic(dep);
vs = dd1(:, 2);
vp = dd1(:, 3);
den = dd1(:, 4);
fv = load("K:\Hangzhou_Fengqi_case-detectionLVL\1st suggestion major\APPENDIX\69.sw_DispersionCurve_Measured.txt");
f = fv(:, 1);
vr = mat_disperse(thic, den, vp, vs, f);
hold on;
plot(f, vr, 'black');
plot(f, fv(:, 2), 'r');
hold off;
% SE-67
subplot(3, 1, 3);
dd1 = load("K:\Hangzhou_Fengqi_case-detectionLVL\1st suggestion major\APPENDIX\67.sw_InvertedModel-use.txt");
dep = dd1(:, end);
thic = dep2thic(dep);
vs = dd1(:, 2);
vp = dd1(:, 3);
den = dd1(:, 4);
fv = load("K:\Hangzhou_Fengqi_case-detectionLVL\1st suggestion major\APPENDIX\67.sw_DispersionCurve_Measured.txt");
f = fv(:, 1);
vr = mat_disperse(thic, den, vp, vs, f);
hold on;
plot(f, vr, 'black');
plot(f, fv(:, 2), 'r');
hold off;



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
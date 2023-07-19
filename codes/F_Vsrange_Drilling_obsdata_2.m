function [range_vs_2] = F_Vsrange_Drilling_obsdata_2(obsdata, dri_1, dri_2, ini, up, down, limte)
%UNTITLED weak constraint
% obsdata 观测数据
% up 上限
% down 下限
% limte 极限
% dri_1, dri_2 raw drilling data
% ini depth

% dep = ini(:, 5);
% dep = [dep; 90];
layers = 16;
dep = [0;5;10;15;20;25;30;35;40;45;50;55;60;65;70;80;90];
dri = [dri_1; dri_2];
med = zeros(layers, 3);
for i = 1 : layers
    loc = find(dri(:, 1) >= dep(i) & dri(:, 1) <= dep(i + 1));
    all = dri(loc, 2);
    med(i, 1) = median(all);
end

med_obv = zeros(layers, 1);
for i = 1 : layers
    loc = find(obsdata(:, 1) >= dep(i) & obsdata(:, 1) <= dep(i + 1));
    all = obsdata(loc, 2);
    med_obv(i, 1) = median(all);
end

% plot(obsdata(:, 1), obsdata(:, 2), 'b*');
% hold on;
% plot(dri(:, 1), dri(:, 2), 'r');
% hold off;
% figure(2);
% hold on
% plot(1:12, med(:, 1), 'r');
% plot(1:12, med_obv(:, 1), 'b');
med(1:5, 1) = med_obv(1:5, 1);
med(end, 1) = 1000;
%% *************************************************************** 
if(nargin == 7)
    for i = 1 : 7
        v2 = med(i, 1) * (up * 0.01);
        v3 = med(i, 1) * (down * 0.01);
        limte =  med(i, 1) * (10 * 0.01);
        if(v2 < limte)
            med(i, 2) = med(i, 1) - v2;
        else
            med(i, 2) = med(i, 1) - limte;
        end
        if(v3 < limte)
            med(i, 3) = med(i, 1) + v3;
        else
            med(i, 3) = med(i, 1) + limte;
        end
    end
    for i = 8 : 12
        v2 = med(i, 1) * (up * 0.01);
        v3 = med(i, 1) * (down * 0.01);
        limte =  med(i, 1) * (50 * 0.01);
        if(v2 < limte)
            med(i, 2) = med(i, 1) - v2;
        else
            med(i, 2) = med(i, 1) - limte;
        end
        if(v3 < limte)
            med(i, 3) = med(i, 1) + v3;
        else
            med(i, 3) = med(i, 1) + limte;
        end
    end
    for i = 13 : layers
        v2 = med(i, 1) * (up * 0.01);
        v3 = med(i, 1) * (down * 0.01);
        limte =  med(i, 1) * (30 * 0.01);
        if(v2 < limte)
            med(i, 2) = med(i, 1) - v2;
        else
            med(i, 2) = med(i, 1) - limte;
        end
        if(v3 < limte)
            med(i, 3) = med(i, 1) + v3;
        else
            med(i, 3) = med(i, 1) + limte;
        end
    end
end
if(nargin == 6)
    med(:, 3) = med(:, 1) .* (1 + up * 0.01);
    med(:, 2) = med(:, 1) .* (1 - down * 0.01);
end
%% ***************************************************************
range_vs_2 = med;
save('cc_vs_weak.mat', 'range_vs_2');
end




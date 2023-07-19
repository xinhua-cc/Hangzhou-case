function [] = F_Simulate_2(ini, all_range_vs, path1, path2, sta, fin)
% ini load initial model
% range_vs 随机范围
% path1， path2 存储路径
% sta, fin 生成文件范围
%
H = 90;
layers = 16;
dep = [0;5;10;15;20;25;30;35;40;45;50;55;60;65;70;80;90];
thic = dep2thic(dep); % lack the final layer
thic(end) = [];
den = 2 * ones(layers, 1);
f = 1.8: 0.1 : 19.5;
% simulate
i = 1;
range_vs = all_range_vs(:, 2:3);
range_vs = fix(range_vs);
m_density = 1;
parfor i = sta : fin
    disp(i);
    % randomly generate vs within its ranges
    flag = 1;
    while(flag)
        Vs = zeros(layers, 1);
        %         Vs(1) = prorandi(range_vs(1, 1), fix(0.5*(range_vs(1, 1)+range_vs(1, 2))), range_vs(1, 2), 65);
        Vs(1) = randi([range_vs(1, 1), range_vs(1, 2)]);
        % ensure 2-6 is incremental model
        for j = 2 : 5
            v1 = max(fix(range_vs(j, 1)), Vs(j - 1));
            Vs(j) = randi([v1, ceil(range_vs(j, 2))]);
        end
        
        for j = 6 : 10
            v11 = fix(range_vs(j, 1));
            v1 = max(v11, Vs(j - 1));
            v21 = fix(range_vs(j, 2));
            v22 = fix(1.5 * Vs(j - 1));
            v2 = min(v21, v22);
            if v2 >= v1
                Vs(j) = randi([v1, v2]);
            else
                Vs(j) = randi([Vs(j - 1), v22]);
            end
        end
        
        for j = 11 : 12
            v1 = max(fix(range_vs(j, 1)), Vs(1));
            Vs(j) = randi([v1, fix(range_vs(j, 2))]);
        end
        for j = 13 : layers
            v1 = max(fix(range_vs(j, 1)), Vs(j - 1));
            Vs(j) = randi([v1, fix(range_vs(j, 2))]);
        end
        
        % mean, ensure within the range after mean. if out give up mean
        
        len = 3;
        for j = 1 : 13
            aa = mean(Vs(j : (j + len - 1)));
            bb = std(Vs(j : (j + len - 1)));
            if aa > fix(range_vs(j + fix(len * 0.5), 1)) && aa < fix(range_vs(j + fix(len * 0.5), 2))
                now_vs = Vs(j + fix(len * 0.5));
                dd = abs(aa - now_vs);
                if dd >= (1.2 * bb)
                    Vs(j + fix(len * 0.5)) = aa;
                end
            end
        end
        
        % generate v_phase
        Vp = zeros(layers, 1);
        Vp(1:12) = Vs(1:12) ./ 0.25;
        Vp(13:end) = Vs(13:end) ./ 0.3;
        Vr = mat_disperse(thic, den, Vp, Vs, f);
        % judge the availability
        simulated_maxd = 0.5 * max(Vr ./ f');
        if simulated_maxd >= 80
            aa = corrcoef(Vs(1:8), all_range_vs(1:8, 1));
            bb = aa(1, 2);
            if bb >= 0.9
                for j = 1 : m_density
                    fv = zeros(length(f), 2);
                    fv(:, 1) = f;
                    for k = 1 :length(f)
                        noise = rand(1, 1) * 30 - 15;
                        while(1)
                            if(abs(noise) < 0.1 * Vr(k))
                                break;
                            end
                            noise = rand(1, 1) * 30 - 15;
                        end
                        fv(k, 2) = Vr(k) + noise;
                    end
                    
                    fid = fopen(strcat(path1, num2str((i - 1) * m_density + j), '.txt'), 'w');
                    fprintf(fid,'%f  %f\r\n', fv');
                    fclose(fid);
                    fid = fopen(strcat(path2, num2str((i - 1) * m_density + j), '.txt'), 'w');
                    fprintf(fid,'%f\r\n', Vs');
                    fclose(fid);
                end
                flag = 0;
            else
                flag = 1;
            end
        else
            flag = 1;
        end
    end
end



% H the whole depth
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
% the size of h < depth
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

end

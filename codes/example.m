% Input file for mat_disperse.m

% Define vectors or layer thickness, mass density, shear wave velocity
% and compression wave velocity
thk = [10.0 ];
dns = [2.0 2.0];
vs = [200 400];
vp = [800 1200];

% Define a vector of frequencies (in Hz)
freq = linspace(1,100,100);

% Define a vector of offsets from the source
offsets = linspace(1,60,60);

% Call mat_disperse.m to solve the eigenvalue problem and calculate phase
% velocities, displacement-stress functions, and surface wave displacements
%[vr,z,r,dvrvs,vre,dvrevs,ur,uy] = mat_disperse(thk,dns,vp,vs,freq,offsets);
vr = mat_disperse(thk,dns,vp,vs,freq);
[M,N]=size(vr);
%ph=fopen('E:\ÀíÂÛÆµÉ¢ÇúÏß\mat_disperse\diepersion.txt','w');
ph=fopen('diepersion.txt','w');
for j=1:N
    for i=1:M
      fprintf(ph,'%12.9G %12.9G\n',freq(i),vr(i,j));
    end
end
fclose(ph);

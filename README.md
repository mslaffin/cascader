This repo provides functionality to read and manipulate S-parameter files, including cascading operations on 2 port models. 

The input files must follow the standardized [Touchstone](https://ibis.org/touchstone_ver2.0/touchstone_ver2_0.pdf) file format (`.snp`, where `n` is the number of ports), and contain sets of data representing scattering parameters of linear networks. 

In the particular case of cascading two 2-port S-parameter models, the script will take both sets of parameters (each representing a two port network) and calculates the resulting S-parameters of the combined network as if these two networks were connected in series.

The two port network can be described in the following matrix form:

$$
S = \begin{pmatrix}
S_{11} & S_{12} \\
S_{21} & S_{22}
\end{pmatrix}
$$

Where: 
- S<sub>11</sub> and S<sub>22</sub> are the input and output reflection coefficients , respectively.
- S<sub>21</sub> and S<sub>12</sub> are the forward and reverse transmission coefficients, respectively.

### Cascading formula
The resulting S-parameter matrix can be calculated using the following formulas for each element of the cascaded S-parameter matrix:

$$
S_{11} = S^1_{11} + \frac{S^1_{12} \cdot S^1_{21} \cdot S^2_{11}}{1 - S^2_{11} \cdot S^1_{22}}
$$

$$
S_{12} = \frac{S^1_{12} \cdot S^2_{12}}{1 - S^2_{11} \cdot S^1_{22}}
$$

$$
S_{21} = \frac{S^2_{21} \cdot S^1_{21}}{1 - S^1_{22} \cdot S^2_{11}}
$$

$$
S_{22} = S^2_{22} + \frac{S^2_{21} \cdot S^2_{12} \cdot S^1_{22}}{1 - S^1_{22} \cdot S^2_{11}}
$$

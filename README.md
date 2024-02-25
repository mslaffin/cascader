This repo provides functionality to read and manipulate S-parameter files, including cascading operations on 2 port models. 

The input files must follow the standardized [Touchstone](https://ibis.org/touchstone_ver2.0/touchstone_ver2_0.pdf) file format (`.snp`, where `n` is the number of ports), and contain sets of data representing scattering parameters of linear networks. 

### Using two 2-port S-parameter models
![top level diagram](https://github.com/mslaffin/cascader/blob/main/media/top_level_diagram.png)
In this particular case, the script will read both files, extract both sets of parameters (each representing a two port network) and calculate the result parameters as if these two networks were connected in series. The cascading algorithm I used here utilizes a generalized two port chain scattering model. Read more this model [here](https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electronics/Microwave_and_RF_Design_III_-_Networks_(Steer)/02%3A_Chapter_2/2.4%3A_Generalized_Scattering_Parameters)

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

- Note that the input and output of each network affects the other.
- The division by $1 - S^2_{11} \cdot S^1_{22}$ or $1 - S^1_{22} \cdot S^2_{11}$ in these formulas accounds for this interaction between the two networks, improving the accuracy of the combined network's behavior. 

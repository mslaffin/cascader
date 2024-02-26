This repo provides functionality to read and manipulate S-parameter files, including cascading operations on 2 port models. 

The input files must follow the standardized [Touchstone](https://ibis.org/touchstone_ver2.0/touchstone_ver2_0.pdf) file format (`.snp`, where `n` is the number of ports), and contain sets of data representing scattering parameters of linear networks. 

Process Summary:

1. Read S-parameter files, validate format
2. Verify all S-parameter sets are defined over the same frequency points. If not, interpolate.
3. Conversion to T parameters (for 3-port networks): NOT IMPLEMENTED
4. Cascading: Perform cascading matrix operation
5. Back Conversion (for 3-port networks): NOT IMPLEMENTED

### Cascading algorithm
![top level diagram](https://github.com/mslaffin/cascader/blob/main/media/top_level_diagram.png)
The script will read both files, extracting sets of parameters (each representing a two port network component) and calculates a resulting parameter set as if these two networks were connected in series. The cascading algorithm directly embeds the combined network response into a single whole network. This approach utilizes a generalized two port chain scattering model and system of network embedding equations. Read more this model from LibreTexts [here](https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electronics/Microwave_and_RF_Design_III_-_Networks_(Steer)/02%3A_Chapter_2/2.4%3A_Generalized_Scattering_Parameters), and the embedding equations from RFCafe [here](https://www.rfcafe.com/references/articles/Joe-Cahak/Computing-Scattering-Parameters.htm).

![cascade diagram with coefficients](https://github.com/mslaffin/cascader/blob/main/media/cascade_diagram_with_coefficients.png)

The two port networks from the above figure can be described in the following matrix form:

$$
S = \begin{pmatrix}
S_{11} & S_{12} \\
S_{21} & S_{22}
\end{pmatrix}
$$

Where: 
- S<sub>11</sub> and S<sub>22</sub> are the input and output reflection coefficients , respectively.
- S<sub>21</sub> and S<sub>12</sub> are the forward and reverse transmission coefficients, respectively.

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
- The division by $1 - S^2_{11} \cdot S^1_{22}$ or $1 - S^1_{22} \cdot S^2_{11}$ in these formulas accounds for this interaction between the two networks.

Here is the corresponding implementation inside `cascade_s2p`:
```python
        s11 = s1[i][0,0] + (s1[i][0,1] * s1[i][1,0] * s2[i][0,0]) / (1 - s2[i][0,0] * s1[i][1,1])
        s12 = (s1[i][0,1] * s2[i][0,1]) / (1 - s2[i][0,0] * s1[i][1,1])
        s21 = (s2[i][1,0] * s1[i][1,0]) / (1 - s1[i][1,1] * s2[i][0,0])
        s22 = s2[i][1,1] + (s2[i][1,0] * s2[i][0,1] * s1[i][1,1]) / (1 - s1[i][1,1] * s2[i][0,0])
```



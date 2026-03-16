# **Linear attention is** (maybe) **all you need**  
(to understand transformer optimization)

## Abstract

Transformer training is notoriously difficult, requiring a careful design of optimizers and use of various heuristics. We make progress towards understanding the subtleties of training transformers by carefully studying a simple yet canonical linearized *shallow* transformer model. Specifically, we train linear transformers to solve regression tasks, inspired by J. von Oswald *et al.* (ICML 2023), and K. Ahn et al. (NeurIPS 2023). Most importantly, we observe that our proposed linearized models can reproduce several prominent aspects of transformer training dynamics. Consequently, the results obtained in this paper suggest that a simple linearized transformer model could actually be a valuable, realistic abstraction for understanding transformer optimization.

maketitle thanks aketitle

# Introduction

Transformer architectures  (henceforth, referred to as *transformers*) have shown impressive performance in various applications . However, training transformers is notoriously difficult and laborious; see, e.g., observations given by as well as scaling laws . In particular, training transformers requires carefully designed optimizers as well as use of various heuristics. For instance, as illustrated in <a href="#fig:motivation" data-reference-type="ref+label" data-reference="fig:motivation">1</a>, stochastic gradient descent (SGD)—the workhorse of most deep learning optimization problems—fails to train transformers effectively. This failure is in contrast to the success of SGD when applied to train convolutional neural networks (CNNs) on vision tasks.

Several recent papers propose a number of different explanations as to why transformer optimization is so difficult. There is a general consensus in the literature that the loss landscape of transformers has a number of distinctive features that significantly differ from standard optimization theory assumptions. Most notably, it is empirically verified through various experiments that stochastic gradient noise is heavy-tailed and non-Gaussian  and the loss landscape is significantly ill-conditioned . In particular, standard assumptions are incapable of dealing with and explaining these observations, and as a result, transformer optimization has become more of an art than science.

A major obstacle in understanding transformer optimization is that full-fledged transformers are extremely complicated to model. One can probe the transformer’s properties by measuring quantities, such as gradient norm or smoothness, but it is much harder to parse the inner-layer workings, and to satisfactorily answer questions such as: *why* does the loss landscape have such features, or *how* do algorithms like Adam perform better than SGD in transformer training?

For these reasons, having an appropriate *mathematical abstraction* is necessary for progress in understanding transformer optimization — an abstraction that is as simple as possible, while still able to capture the essence of transformer optimization. The main message of this paper is that these distinctive features of transformer training also arise in a far simpler setting: we propose that the *linear attention model* is precisely the abstraction that we are looking for. We verify that training this model on a low-dimensional linear regression task displays all the distinctive features that have been observed on the full transformer, suggesting that our surprisingly simple model can serve as a testbed for rigorous understanding of transformer optimization.

#### Main contributions.

We summarize our main contributions as follows:

- We propose the problem of *training shallow linear transformer model on random linear regression* as a model for understanding transformer optimization. We verify that this model reproduces all the optimization features and phenomena that have been previously reported for full transformers.

- We leverage the simplicity of our model to look deeper into how these features arise, by changing settings (e.g., data distribution, the number of layers). Our results reveal that the unique features from previous work get more pronounced in our linear transformer setting when the data distribution becomes more heavy-tailed, or the number of layers increases.

As a preliminary to our discussion, we first survey the previous works that seek to characterize and understand the transformer optimization landscape.

# Distinctive features of transformer optimization

Numerous recent papers have identified a number of distinctive features of the transformer optimization problem, which set it apart from commonly studied optimization objectives, or even other neural networks such as CNNs. As shown in <a href="#fig:motivation" data-reference-type="ref+label" data-reference="fig:motivation">1</a>, one of the most striking features is the following:
``` math
\begin{aligned}
 \tag{Adam$>$SGD}
\boxed{\text{Adaptive method like {\bf Adam are significantly better than SGD}!}} \label{adam}
\end{aligned}
```
This is in stark contrast with the training of other neural networks (e.g., convolutional neural networks) for which several works have shown that the values of adaptive methods are marginal . This phenomenon sparked the interest of the optimization community in investigating the main causes, and subsequently, recent works have identified various “unique” features of transformer optimization.

<figure id="fig:motivation">
<img src="./figures/legends_standard.png"" />
<figure>
<img src="./figures/cnns.png"" />
<figcaption><span><strong>CNNs</strong></span> on MNIST and CIFAR-10</figcaption>
</figure>
<figure>
<img src="./figures/transformers.png"" />
<figcaption><span><strong>Transformers</strong></span> on PTB, WikiText2, and SQuAD</figcaption>
</figure>
<figcaption><span> Adaptive optimization methods like Adam are much more effective than SGD for training transformers.</span> This experimental result is taken from <span class="citation" data-cites="kunstner2023noise"></span>. (+m) denotes "with momentum".</figcaption>
</figure>

<figure id="fig:dir_smoothness_vs_iter">
<div class="mdframed">
<div class="center">
<p><span><strong>Transformers (in practice)</strong></span></p>
</div>
<div class="center">
<p><span><strong>Shallow linear transformers</strong></span></p>
</div>
<div class="center">
<p><span style="color: white"> Easter Egg</span></p>
</div>
<div class="center">
<p><span> (see <a href="#sec:setting" data-reference-type="ref+label" data-reference="sec:setting">3.1</a> and <a href="#table:setting" data-reference-type="ref+label" data-reference="table:setting">1</a>)</span></p>
</div>
<p><u><strong>1. Gap between Adam v.s SGD <span><span class="citation" data-cites="zhang2020adaptive kunstner2023noise jiang2022does pan2023toward"></span></span>:</strong></u><br />
<img src="./figures/legends_standard.png"" /></p>
<div class="center">
<img src="./figures/transformers.png"" />
</div>
<div class="center">
<p><img src="./figures/gaussian_loss.png"" style="width:32.0%" /> <img src="./figures/gaussian_loss_N5.png"" style="width:32.0%" /> <img src="./figures/gamma_loss.png"" style="width:32.0%" /></p>
</div>
<p><u><strong>2. Heavy-tailed stochastic gradient noise <span><span class="citation" data-cites="zhang2020adaptive kunstner2023noise"></span></span>:</strong></u><br />
<img src="./figures/noise_histogram.png"" /></p>
<p><img src="./figures/gaussian_heavy_tail_noise_N20.png"" style="width:32.0%" /> <img src="./figures/gaussian_heavy_tail_noise_N5.png"" style="width:32.0%" /> <img src="./figures/gamma_heavy_tail_noise_zoom.png"" style="width:32.0%" /></p>
<p><u><strong>3. Robust condition number of the landscape <span><span class="citation" data-cites="jiang2022does"></span></span>:</strong></u><br />
</p>
<table>
<tbody>
<tr>
<td rowspan="2" style="text-align: center;">Layer#</td>
<td style="text-align: center;"><span><strong>Iteration 750</strong></span></td>
<td style="text-align: center;"><span><strong>Iteration 1250</strong></span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">$\nicefrac{R^{\sf SGD}_{\sf med}}{R^{\sf Adam}_{\sf med}}$</span></td>
<td style="text-align: center;"><span class="math inline">$\nicefrac{R^{\sf SGD}_{\sf med}}{R^{\sf Adam}_{\sf med}}$</span></td>
</tr>
<tr>
<td style="text-align: center;">15</td>
<td style="text-align: center;">1.65 (0.65)</td>
<td style="text-align: center;">2.01 (1.00)</td>
</tr>
<tr>
<td style="text-align: center;">17</td>
<td style="text-align: center;">1.91 (0.53)</td>
<td style="text-align: center;">1.43 (0.63)</td>
</tr>
<tr>
<td style="text-align: center;">22</td>
<td style="text-align: center;">3.54 (1.21)</td>
<td style="text-align: center;">2.28 (1.18)</td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>
<td rowspan="2" style="text-align: center;"></td>
<td style="text-align: center;"><span><strong>Iteration 750</strong></span></td>
<td style="text-align: center;"><span><strong>Iteration 1250</strong></span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="math inline">$\nicefrac{R^{\sf SGD}_{\sf med}}{R^{\sf Adam}_{\sf med}}$</span></td>
<td style="text-align: center;"><span class="math inline">$\nicefrac{R^{\sf SGD}_{\sf med}}{R^{\sf Adam}_{\sf med}}$</span></td>
</tr>
<tr>
<td style="text-align: center;">Setting 1</td>
<td style="text-align: center;">1.76 (0.40)</td>
<td style="text-align: center;">1.58 (0.41)</td>
</tr>
<tr>
<td style="text-align: center;">Setting 2</td>
<td style="text-align: center;">3.14 (0.97)</td>
<td style="text-align: center;">5.98 (2.86)</td>
</tr>
<tr>
<td style="text-align: center;">Setting 3</td>
<td style="text-align: center;">9.57 (13.3)</td>
<td style="text-align: center;">6.53 (3.55)</td>
</tr>
</tbody>
</table>
<p><u><strong>4. Directional smoothness gap between SGD v.s Adam <span><span class="citation" data-cites="zhang2019gradient pan2023toward"></span></span>:</strong></u><br />
<span id="fig:dir_smoothness_vs_iter" data-label="fig:dir_smoothness_vs_iter"></span></p>
<p><img src="./figures/dir_smoothness_iter_20_normal-3.png"" style="width:32.0%" /> <img src="./figures/dir_smoothness_iter_5_normal-1.png"" style="width:32.0%" /> <img src="./figures/dir_smoothness_iter_20_gamma-1.png"" style="width:32.0%" /></p>
</div>
<figcaption> The comparison of the robust condition number (see <a href="#jiang2022does" data-reference-type="ref+label" data-reference="jiang2022does">2.3</a>) between SGD and Adam for transformer optmization. Numbers in parentheses show standard deviation. Left table: Full transformers, from <span class="citation" data-cites="jiang2022does"></span>. Right table: Shallow linear transformers, see <a href="#table:setting" data-reference-type="ref+label" data-reference="table:setting">1</a>.</figcaption>
</figure>

In this section, we discuss them one by one in detail, building preliminaries for our main results. In order to discuss each feature, we first give a whirlwind tour on some background in optimization – see, e.g., monographs for greater contexts.

## A whirlwind tour of (convex) optimization theory

For a symmetric matrix $`M`$, we denote by $`\lambda_{\max}(M)`$ and $`\lambda_{\min}(M)`$ the largest and smallest eigenvalue of $`M`$, and by $`M_2`$ the spectral norm of $`M`$. For simplicity, we assume the training loss function $`f`$ is twice differentiable. We introduce the following standard concepts in the optimization literature.

- **Lipschitzness.** We say $`f`$ is $`G`$-Lipschitz if $`\nabla f_2 \leq G`$.

- **Smoothness.** We say $`f`$ is $`L`$-smooth if $`\nabla^2 f_2 \leq L`$.

- **Strong convexity.** We say $`f`$ is $`\mu`$-strongly convex if $`\lambda_{\min}(\nabla^2 f) \geq \mu`$.

- **Condition number.** The (local) condition number $`\kappa_f(x)`$ is defined as $`\nicefrac{\lambda_{\max}(\nabla^2 f(x))}{ \lambda_{\min}(\nabla^2 f(x))}`$, provided that $`\lambda_{\min}(\nabla^2 f(x))>0`$.

- **Bounded stochastic gradient noise.** In most SGD analyses, it is assumed that the stochastic gradient $`g(x)`$ satisfies the *bounded variance* property: $`\mathbb{E}g(x)-\nabla f(x)^2 \leq \sigma^2`$.

The features defined above are typically of great importance in the theory of convex optimization, as the convergence rate of gradient-based optimizers (e.g., gradient descent) typically depends on these quantities. For instance, the convergence rate of gradient descent gets better as the Lipschitzness or smoothness constant gets smaller, or the condition number gets smaller . Building on these concepts, we now discuss the previous studies on transformer optimization. Several recent works have connected the difficulties of training transformers to the unconventional features arising from the loss landscape of transformer optimization.

## Heavy-tailed gradient noise 

In (entitled *Why are adaptive methods good for attention models?*), it was observed that the stochastic gradient is typically more heavy-tailed for transformer optimization than other neural network optimization. In particular, they make a case that this is opposed to the standard bounded variance condition for SGD analysis – see <a href="#fig:histogram" data-reference-type="ref+label" data-reference="fig:histogram">[fig:histogram]</a> and <a href="#fig:histogram_more" data-reference-type="ref+label" data-reference="fig:histogram_more">3</a>. They posit that this phenomenon might be one of the main reasons behind the phenomenon <a href="#adam" data-reference-type="eqref" data-reference="adam">[adam]</a>; they also theoretically show that adaptive step sizes in the form of gradient clipping is required for convergence.

<figure id="fig:histogram_more">
<img src="./figures/histogram_full.png"" style="width:80.0%" />
<figcaption> <span><strong>The heavy-tail stochastic gradient noise for transformers.</strong></span> Under the same setting as <a href="#fig:motivation" data-reference-type="ref+label" data-reference="fig:motivation">1</a>, <span class="citation" data-cites="kunstner2023noise"></span> plot the stochastic gradient noise at the initialization. Notice that the stochastic gradient noise for the convolutional neural networks on vision tasks (MNIST, CIFAR-10) is much less heavy-tailed than the transformers on NLP tasks. We will revisit this plot in <a href="#fig:histogram_2" data-reference-type="ref+label" data-reference="fig:histogram_2">[fig:histogram_2]</a> with shallow linear transformers. </figcaption>
</figure>

A noteworthy follow-up work by reveal that the heavy-tailed stochastic noise may not explain the full picture. In particular, they compare the full-batch versions (hence no stochastic noise), and notice the phenomenon <a href="#adam" data-reference-type="eqref" data-reference="adam">[adam]</a> still hold. Since there is no stochastic noise in this setting, the explanation based on heavy-tailed noise does not apply here.

## Ill-conditioned landscape 

In another inspiring work by , authors seek to understand the difficulty of transformer optimization through the lens of condition number. In particular, they consider a “robust” version of condition number defined as $`R^{\sf OPT}_{\sf med}\coloneqq\nicefrac{\lambda_{\max}(\nabla^2 f)}{\lambda_{\text{median}}(\nabla^2 f)}`$[^1], and here the reason for $`\lambda_{\text{median}}`$ instead of $`\lambda_{\min}`$ is to handle the case where the Hessian is degenerate. They observe that during transformer optimization, non-adaptive optimizers like SGD tend to have larger robust condition number than adaptive optimizers like Adam; they posit that this phenomenon is one of the main reasons for <a href="#adam" data-reference-type="eqref" data-reference="adam">[adam]</a> – see <a href="#table:robust" data-reference-type="ref+label" data-reference="table:robust">[table:robust]</a>. also report that this gap is not there when training convolutational neural networks on image classfication tasks, and suggest that this phenomenon may be rooted in unique features of the transformer which are missing in other popular neural networks.

## Directional Smoothness 

In a follow up work by (entitled *Toward understanding why Adam converges faster than SGD for transformers*), the authors again corroborate <a href="#adam" data-reference-type="eqref" data-reference="adam">[adam]</a>. In addition, they further observe in that proper gradient clipping techniques further accelerate optimization. In order to understand this phenomenon, they propose an explanation based on “directional smoothnesss” along the iterates $`x_t`$. More formally, they consider the following Taylor expansion along the iterates:
``` math
\begin{aligned}
&f(x_{t+1}) - f(x_t) =   \nabla f(x_t)^\top (x_{t+1} - x_t)  + \frac{1}{2}  (x_{t+1} - x_t)^\top \nabla^2 f(x_t)(x_{t+1} - x_t)  + O(\eta^3)\,,
\label{eq:taylor}
\end{aligned}
```
and define the directional smoothness as . In particular, based on the above calculations, one can infer that smaller directional smoothness implies better optimization as $`f(x_{t+1}) - f(x_t)`$ becomes smaller. They claim that the directional smoothness holds the key to understanding <a href="#adam" data-reference-type="eqref" data-reference="adam">[adam]</a> (as well as transformer optimization in general). They also verify that adaptive optimizers tend to have smaller directional smoothness values, and employing gradient clipping further reduces the directional smoothness. Once again, hypothesize that this feature is unique to transformers, as they observe that adaptive algorithms can demonstrate *worse directional smoothness* than SGD for, e.g., ResNet training.

## Generalized smoothness 

We discuss one more noteworthy work  that identifies another unconventional feature. Here we highlight that the main motivation of was not about understanding <a href="#adam" data-reference-type="eqref" data-reference="adam">[adam]</a>, and they also observe their proposed feature in some other non-transformer neural networks such as ResNet. The main observation made by is that the standard smoothness assumption is not suitable for neural network training. Instead, they observed that the spectral norm of Hessian typically grows with the norm of gradient at the current iterate (see <a href="#fig:smoothness" data-reference-type="ref+label" data-reference="fig:smoothness">6</a>). Based on this observation, the authors define the following notion of generalized smoothness:

<div id="def:gen_smooth" class="definition">

**Definition 1**. *We say $`f`$ is $`(L_0,L_1)`$-smooth if $`\nabla^2 f(x) \leq L_0 + L_1\nabla f(x)`$. When $`L_1=0`$, this condition recovers the standard smoothness condition.*

</div>

A coordinate-wise version of <a href="#def:gen_smooth" data-reference-type="ref+label" data-reference="def:gen_smooth">1</a> was considered in . Under <a href="#def:gen_smooth" data-reference-type="ref+label" data-reference="def:gen_smooth">1</a>, they demonstrate that non-adaptive SGD needs more iterations to converge than an adaptive method based on the global clipping of gradients.

Thus far, we have seen several features identified in the previous works that set transformer optimization apart from other neural network optimizations. In the next section, we propose a simple yet canonical transformer model that exhibits all these features.

# Linear shallow transformers have the same loss landscape as practical deep transformers

In this section, we show that a simple yet canonical transformer model exhibits all the features in <a href="#sec:features" data-reference-type="ref+label" data-reference="sec:features">2</a>. Specifically, the optimization problem to be solved is the training of **linear transformers on random instances of linear regression**, a model recently proposed for understanding of in-context learning .

## Linear transformer on linear regression

#### Data distribution.

The data distribution can be thought of as the random instances of linear regression. Concretely, let $`X \in \mathbb{R}^{(n+1)\times d}`$ be the matrix of covariates of the regression whose row $`i`$ contains tokens $`{i} \in \mathbb{R}^d`$ drawn i.i.d. from a distribution $`D_{\mathcal{X}}`$. We then draw $`w_\star\sim D_{\mathcal{W}}`$ and then generate the scalar responses $`y = [ \langle1, w_\star\rangle,\dots,  \langle n,w_\star\rangle] \in \mathbb{R}^n`$. Now the input of the data set consists of these linear regression examples:
``` math
\begin{aligned}
\label{exp:input}
\text{Input matrix:}~~   Z_0 = \begin{bmatrix}
1 & 2 & \cdots & n &n+1 \\ 
1 & 2 & \cdots &n& 0
\end{bmatrix} \in \mathbb{R}^{(d+1) \times (n+1)}\,.
\end{aligned}
```
The goal is to predict the missing $`n+1`$, as we detail below.

#### Optimization objective.

Let $`{\sf TF}_L(\cdot ; W): \mathbb{R}^{(n+1) \times (d+1)} \to \mathbb{R}`$ denote the prediction of the linear transformer with parameters $`W`$. Our optimization objective is given by
``` math
\begin{aligned}
    f\left(W\right) := \mathbb{E}_{(Z_0,w_\star)} \Bigl[ \left(  {\sf TF}_L(Z_0; W)  - w_\star^\top n+1  \right)^2\Bigr]\,.
\end{aligned}
```
In words, we train the linear transformer to predict $`n+1`$ using $`{\sf TF}_L(Z_0; W)`$; we will formally define the linear transformer architecture below. This objective was the center of study in a number of recent empirical and theoretical works on understanding transformers .

#### Linear transformer (self-attention) architecture.

We will now present the neural network architecture that will be used throughout this paper. Given matrices $`P, Q \in \mathbb{R}^{(d+1)\times (d+1)}`$, we define the **linear self-attention** architecture as
``` math
\begin{aligned}
 \label{eq:linear}
{\sf Attn}_{P,Q}(Z) = P Z M(Z^\top Q Z) \quad \text{where} ~~M\coloneqq\begin{bmatrix} I_n & 0 \\0 & 0 \end{bmatrix} \in \mathbb{R}^{(n+1) \times (n+1)}\,.
\end{aligned}
```
Finally, for a positive integer $`L`$, we define an **$`L`$-layer linear transformer $`{\sf TF}_L`$** as a stack of $`L`$ linear attention units. Specifically, let the output of the $`L^{\text{th}}`$ layer attention, $`Z_L`$, be recursively defined as
``` math
\begin{aligned}
 \label{eq:recursion}
Z_{\ell+1} = Z_{\ell} +\frac{1}{n}  {\sf Attn}_{P_\ell,Q_\ell}(Z_\ell)\quad \text{for $\ell=0,1,\dots,L-1$}. 
\end{aligned}
```
Then we define $`{\sf TF}_L (Z_0; \{P_\ell,Q_\ell\}_{\ell=0}^{L-1})  = -[Z_{L}]_{(d+1),(n+1)}`$, i.e., the $`(d+1,n+1)`$-th entry of $`Z_{\ell}`$. The reason for the minus sign is to be consistent with , where such a choice was motivated by theoretical considerations.

<figure id="fig:softmax">
<img src="./figures/softmax.png"" style="width:25.0%" />
<figcaption><span class="math inline">log (loss)</span> against iteration. Comparison between linear attention and softmax attention for the 3-layer transformers. Note that the loss of linear transformer decreases much faster.</figcaption>
</figure>

We emphasize here that the linear attention unit, defined in <a href="#eq:linear" data-reference-type="eqref" data-reference="eq:linear">[eq:linear]</a>, differs from the standard attention unit in  in two ways: we use a single matrix $`Q`$ to represent the product of key, query matrices, and more importantly, *we remove the softmax activation outside $`Z^\top Q Z`$*. There are two key reasons for our choice:

1.  The linear attention unit is *much better suited to the task of linear regression.* For instance, demonstrates that the performance of softmax transformer with twice many heads matches that of linear transformers; in other words, we need two softmax attention heads to recover the performance of a single linear head. In <a href="#fig:softmax" data-reference-type="ref+label" data-reference="fig:softmax">4</a>, we show that linear attention performs significantly better than standard attention with softmax.

2.  Our goal in this paper is to *find the simplest abstraction* which is representative of the transformer’s optimization landscape. As we will see in <a href="#sec:linear_features" data-reference-type="ref+label" data-reference="sec:linear_features">3.2</a>, the loss landscape of the linear transformer well approximates that of the actual transformer, even without the softmax activation.

## Linear transformers as a fruit abstraction

<div class="center">

<div id="table:setting">

<table>
<caption>Settings for (the right-side plots of) Figures <a href="#fig:sgdadam" data-reference-type="ref" data-reference="fig:sgdadam">[fig:sgdadam]</a>, <a href="#fig:histogram" data-reference-type="ref" data-reference="fig:histogram">[fig:histogram]</a>, <a href="#table:robust" data-reference-type="ref" data-reference="table:robust">[table:robust]</a>, <a href="#fig:dir_smoothness_vs_iter" data-reference-type="ref" data-reference="fig:dir_smoothness_vs_iter">2</a>, and <a href="#fig:smoothness" data-reference-type="ref" data-reference="fig:smoothness">6</a>. </caption>
<tbody>
<tr>
<td rowspan="2" style="text-align: center;">(<span class="math inline"><em>d</em> = 5</span>)</td>
<td style="text-align: center;"><span><strong>Setting 1</strong> </span></td>
<td style="text-align: center;"><span><strong>Setting 2</strong></span></td>
<td style="text-align: center;"><span><strong>Setting 3</strong></span></td>
</tr>
<tr>
<td style="text-align: center;"><span class="citation" data-cites="ahn2023transformers"></span></td>
<td style="text-align: center;">(less covariates)</td>
<td style="text-align: center;">(heavy-tailed covariates)</td>
</tr>
<tr>
<td style="text-align: center;">#contexts <span class="math inline"><em>n</em></span></td>
<td style="text-align: center;">20</td>
<td style="text-align: center;">5</td>
<td style="text-align: center;">20</td>
</tr>
<tr>
<td style="text-align: center;">distribution of <span class="math inline"><em>i</em></span></td>
<td style="text-align: center;"><span class="math inline">𝒩(0, <em>I</em><sub><em>d</em></sub>)</span></td>
<td style="text-align: center;"><span class="math inline">𝒩(0, <em>I</em><sub><em>d</em></sub>)</span></td>
<td style="text-align: center;"><span class="math inline">$\sqrt{\Gamma_{0.1,10
}}\cdot \text{Unif}(\mathbb{S}^{d-1})$</span></td>
</tr>
<tr>
<td style="text-align: center;">distribution of <span class="math inline"><em>w</em><sub>⋆</sub></span></td>
<td style="text-align: center;"><span class="math inline">𝒩(0, <em>I</em><sub><em>d</em></sub>)</span></td>
<td style="text-align: center;"><span class="math inline">𝒩(0, <em>I</em><sub><em>d</em></sub>)</span></td>
<td style="text-align: center;"><span class="math inline">𝒩(0, <em>I</em><sub><em>d</em></sub>)</span></td>
</tr>
</tbody>
</table>

</div>

</div>

**Setting for the experiments.** Having established the framework in <a href="#sec:setting" data-reference-type="ref+label" data-reference="sec:setting">3.1</a>, we now describe details of our experiments. Our base-setup is the 3-layer linear transformer, with 5-dimensional covariates, i.e. $`(L=3,d=5)`$. This is the minimally complex setting that still recovers all of the discussed features of full transformers. Transformers with larger $`L`$ or $`d`$ are qualitatively similar to the $`(L=3, d=5)`$ setting, and we provide such an example in <a href="#fig:diff_Nd" data-reference-type="ref+label" data-reference="fig:diff_Nd">5</a>.

Our “default” setup is Setting 1 of <a href="#table:setting" data-reference-type="ref+label" data-reference="table:setting">1</a>, where the context consists of 20 context demonstrations; each context covariate is sampled from the standard Gaussian, i.e., $`{i} \sim   \mathcal{N}(0,I_d)`$, and we draw $`w_\star\sim \mathcal{N}(0,I_d)`$. This is consistent with previous works  .

<figure id="fig:diff_Nd">
<p><img src="./figures/loss_depth_8_d20.png"" style="width:18.0%" /> <img src="./figures/heavy_tail_noise_depth_8_d20_N60.png"" style="width:18.0%" /></p>
<figcaption>Plots for 8-layer linear transformer with covariate dimension <span class="math inline"><em>d</em> = 20</span> and context length <span class="math inline"><em>n</em> = 60</span>. Left: log(loss) against iterations. Right: histogram of stochastic gradient noise at Epoch 0.</figcaption>
</figure>

In order to understand the effect of context length, we also consider the setting when context length $`n=5`$ instead; this is Setting 2 of <a href="#table:setting" data-reference-type="ref+label" data-reference="table:setting">1</a>.

Finally, to investigate the effect of heavy-tailed covariates on various aspects of the loss landscape, we consider Setting 3 in <a href="#table:setting" data-reference-type="ref+label" data-reference="table:setting">1</a>, where we draw each $`x_i`$ instead uniformly from the unit sphere, and then scale it by the square root of a heavy-tailed Gamma random variable with shape parameter $`k=0.1`$ and scale parameter $`\theta=10`$. Furthermore, in <a href="#sec:data_dist" data-reference-type="ref+label" data-reference="sec:data_dist">4.1</a>, we study the effect of heavy-tailedness of the covariates in more detail.

For each different setting, we pick the best learning rate from a grid search over $`10`$ different choices. We choose the momentum parameter $`0.9`$ for SGD, and $`\beta_1=\beta_2=0.9`$ for Adam. We also employ the (global) gradient clipping where the thresholds are chosen to be $`1`$ for all settings (i.e., the clipped gradient direction is the same as the non-clipped direction). All the experiments are run over $`6`$ different random seeds. See Figures <a href="#fig:sgdadam" data-reference-type="ref" data-reference="fig:sgdadam">[fig:sgdadam]</a>, <a href="#fig:histogram" data-reference-type="ref" data-reference="fig:histogram">[fig:histogram]</a>, <a href="#table:robust" data-reference-type="ref" data-reference="table:robust">[table:robust]</a>, <a href="#fig:dir_smoothness_vs_iter" data-reference-type="ref" data-reference="fig:dir_smoothness_vs_iter">2</a>, and <a href="#fig:smoothness" data-reference-type="ref" data-reference="fig:smoothness">6</a> for the results.

**Discussion of results.** Below we provide detailed discussion of the results.

1.  **Gap between SGD and Adam.** In <a href="#fig:sgdadam" data-reference-type="ref+label" data-reference="fig:sgdadam">[fig:sgdadam]</a> (right), we plot the training loss for the three settings in <a href="#table:setting" data-reference-type="ref+label" data-reference="table:setting">1</a>. Notice that we observe the phenomenon <a href="#adam" data-reference-type="eqref" data-reference="adam">[adam]</a> over three different settings, to different extents. These loss behaviors resemble those of the practical transformer optimization (left plots of <a href="#fig:sgdadam" data-reference-type="ref+label" data-reference="fig:sgdadam">[fig:sgdadam]</a>).

2.  **Heavy-tailed stochastic noise.** In <a href="#fig:histogram" data-reference-type="ref+label" data-reference="fig:histogram">[fig:histogram]</a> (right), following , we plot the stochastic gradient noise at the initialization. Notice the similarity between the left plots and the right plots, showing that the shallow linear transformers also exhibit the heavy-tailed stochastic gradient noise phenomenon.

3.  **Condition number of the landscape.** Following , we measure the “robust” condition numbers of different optimizers along the trajectory. <a href="#table:robust" data-reference-type="ref+label" data-reference="table:robust">[table:robust]</a> shows that the condition numbers of adaptive methods are lower than those of SGD, similar to .

4.  **Directional smoothness.** As observed by previous works , in our experiments, we also observe that Adam has better directional smoothness than SGD, which correlates with the speed-up of Adam over SGD. We present this in <a href="#fig:dir_smoothness_vs_iter" data-reference-type="ref+label" data-reference="fig:dir_smoothness_vs_iter">2</a>.

5.  **Generalized smoothness.** As discussed in <a href="#zhang2019gradient" data-reference-type="ref+label" data-reference="zhang2019gradient">2.5</a>, the generalized smoothness condition of might not be a unique feature to transformer optimization. Nevertheless, interestingly, we also observe such a phenomenon (to a certain extent) in shallow linear transformer optimization as shown in the right plots of <a href="#fig:smoothness" data-reference-type="ref+label" data-reference="fig:smoothness">6</a>.

<figure id="fig:smoothness">
<img src="./figures/smooth_lr30clip025ep1_log-largecap.png"" style="width:100.0%" />
<p><img src="./figures/smoothness_vs_gradnorm_adam_N20_normal_sd1.png"" style="width:32.0%" /> <img src="./figures/smoothness_vs_gradnorm_adam_N5_sd1.png"" style="width:32.0%" /> <img src="./figures/smoothness_vs_gradnorm_adam_N20_gamma_sd1.png"" style="width:32.0%" /></p>
<figcaption>The plot of <span class="math inline">log (∇<em>f</em>(<em>x</em><sub><em>t</em></sub>))</span> against <span class="math inline">log (smoothness)</span>. Following <span class="citation" data-cites="zhang2019gradient"></span>, we measure the directional smoothness instead of <span class="math inline">∥∇<sup>2</sup><em>f</em>(<em>x</em><sub><em>t</em></sub>)∥<sub>2</sub></span>. We observe similar trends with <span class="math inline">∥∇<sup>2</sup><em>f</em>(<em>x</em><sub><em>t</em></sub>)∥<sub>2</sub></span>.<br />
Left plot: LSTM from <span class="citation" data-cites="zhang2019gradient"></span>.<br />
Right 3 plots: Shallow linear transformers trained with Adam, see Settings 1, 2, 3 in <a href="#table:setting" data-reference-type="ref+label" data-reference="table:setting">1</a>.</figcaption>
</figure>

In this section, we have seen that simple linear transformers described in <a href="#sec:setting" data-reference-type="ref+label" data-reference="sec:setting">3.1</a> suffice to recover all the main features identified in previous works (<a href="#sec:features" data-reference-type="ref+label" data-reference="sec:features">2</a>). In the next section, we take advantage of the concreteness and simplicity of our linear transformer to explore and understand the role of heavy-tailedness in data distribution and depth of the network.

# Understanding features based on linear transformers

<figure id="fig:robust_2">
<p><span>0.5</span></p>
<div class="mdframed">
<div class="center">
<p><span><strong>Spherical <span class="math inline"><em>x</em><sup>(<em>i</em>)</sup></span>’s</strong></span></p>
</div>
<div class="center">
<p><span><strong>Heavy-tailed <span class="math inline"><em>x</em><sup>(<em>i</em>)</sup></span>’s</strong></span></p>
</div>
<p><u><strong>1. Comparing SGD v.s Adam:</strong></u></p>
<div class="center">
<img src="./figures/legends_small.png"" style="width:50.0%" />
</div>
<div class="center">
<img src="./figures/loss_depth_3_sphere.png"" style="width:75.0%" />
</div>
<div class="center">
<img src="./figures/gamma_loss.png"" style="width:75.0%" />
</div>
<p><u><strong>2. Stochastic gradient noise:</strong></u></p>
<img src="./figures/sphere_heavy_tail_noise.png"" style="width:70.0%" />
<img src="./figures/gamma_heavy_tail_noise.png"" style="width:70.0%" />
<p><u><strong>3. Robust condition number:</strong></u></p>
<img src="./figures/condition_number_depth_3_sphere.png"" style="width:75.0%" />
<img src="./figures/gamma_condition_number_clip_log.png"" style="width:75.0%" />
</div>
<figcaption> Comparing the robust condition number from <span class="citation" data-cites="jiang2022does"></span></figcaption>
</figure>

The main advantage of our toy linear transformer comes from its simplicity and concreteness. In particular, thanks to the concreteness of the setting, one can conduct various “controlled” experiments to understand the features observed in <a href="#sec:linear_features" data-reference-type="ref+label" data-reference="sec:linear_features">3.2</a>. Recall that the data set used in our experiments consists of nothing but random linear regression instances. This data set is far simpler and more concrete than the language modeling data sets (e.g., Wikipedia texts, question&answering) of the previous works discussed in <a href="#sec:features" data-reference-type="ref+label" data-reference="sec:features">2</a>.

We first take advantage of the concreteness of our data distribution, and look deeper into how the main distinctive features of transformer optimization arise. We first investigate how the “heavy-tailedness” of the data distribution affects the extent of the features from <a href="#sec:features" data-reference-type="ref+label" data-reference="sec:features">2</a>.

## Effect of data distribution

Given that we observe the “heavy-tailedness” of stochastic gradient noise, perhaps a natural question to ask is the following:

***Q.** Does the “heavy-tailedness” of data distribution exacerbate the features in <a href="#sec:features" data-reference-type="ref+label" data-reference="sec:features">2</a>?*

**Settings.** In order to investigate the above question, we consider the following distributions for the covariates $`i`$’s of linear regression:

**- Spherical covariates.** We sample $`i`$’s uniformly at random from the unit sphere $`\mathbb{S}^{d-1}`$.

**- Heavy-tailed covariates.** We first sample $`i`$’s uniformly at random from the unit sphere $`\mathbb{S}^{d-1}`$, and then multiply each covariate by a random scale drawn *i.i.d* from a heavy-tailed distribution, specifically the square root of a Gamma random variable from $`\Gamma_{k,\theta}`$. Note that $`k=2.5`$ and $`\theta =2`$ precisely corresponds to the case where $`i\sim \mathcal{N}(0,I_5)`$. In our experiments, we use $`k=0.1`$ and $`\theta=10`$ to make the distribution more heavy-tailed, while keeping the variance the same.

**Discussion.** We now discuss the experimental results presented in Figures <a href="#fig:sgdadam_2" data-reference-type="ref" data-reference="fig:sgdadam_2">[fig:sgdadam_2]</a>, <a href="#fig:histogram_2" data-reference-type="ref" data-reference="fig:histogram_2">[fig:histogram_2]</a>, and <a href="#fig:robust_2" data-reference-type="ref" data-reference="fig:robust_2">7</a>:

- In <a href="#fig:histogram_2" data-reference-type="ref+label" data-reference="fig:histogram_2">[fig:histogram_2]</a>, we see that “heavy-tailed”-ness of covariates is reflected in the “heavy-tailed”-ness of the stochastic gradient. Notably, the contrast between the two plots in <a href="#fig:histogram_2" data-reference-type="ref+label" data-reference="fig:histogram_2">[fig:histogram_2]</a> reminds us of the contrast we see between CNNs and transformers in <a href="#fig:histogram_more" data-reference-type="ref+label" data-reference="fig:histogram_more">3</a>.

- In <a href="#fig:robust_2" data-reference-type="ref+label" data-reference="fig:robust_2">7</a>, it appears that there is some correlation between the gap in robust condition number, and the “heavy-tailed”-ness of the data distribution, with heavier tails leading to larger gaps.

- Finally, <a href="#fig:sgdadam_2" data-reference-type="ref+label" data-reference="fig:sgdadam_2">[fig:sgdadam_2]</a> shows how the optimization speed of SGD and Adam vary with the heavy-tailedness of covariates. First, given spherical (light-tailed) covariates, both SGD and Adam converge much faster than Gamma-scaled covariates (heavy-tailed). On the other hand, the *relative gap* between the speed of Adam and SGD does not seem to improve noticeably under light-tailed noise.

- Together, <a href="#fig:sgdadam_2" data-reference-type="ref+label" data-reference="fig:sgdadam_2">[fig:sgdadam_2]</a> and <a href="#fig:histogram_2" data-reference-type="ref+label" data-reference="fig:histogram_2">[fig:histogram_2]</a> show that the relationship between heavy-tailed gradient noise and optimization speed may be a little more complicated than suggested in . Specifically, adaptivity seems to be equally beneficial regardless of the heavy-tailedness of the gradient noise. Instead, these two plots seem to align more with the message in – that noise may not be the sole contributor of <a href="#adam" data-reference-type="eqref" data-reference="adam">[adam]</a>.

We next take advantage of the concreteness of our model, and investigate the effect of the number of layers on the optimization.

<figure id="fig:robust_3">
<div class="mdframed">
<div class="center">
<p><span><span class="math inline"><strong>L</strong> <strong>=</strong> <strong>2</strong></span></span></p>
</div>
<div class="center">
<p><span><span class="math inline"><strong>L</strong> <strong>=</strong> <strong>4</strong></span></span></p>
</div>
<div class="center">
<p><span><span class="math inline"><strong>L</strong> <strong>=</strong> <strong>6</strong></span></span></p>
</div>
<div class="center">
<p><span><span class="math inline"><strong>L</strong> <strong>=</strong> <strong>8</strong></span></span></p>
</div>
<p><u><strong>1. Loss against time</strong></u> <img src="./figures/legends_small.png"" style="width:30.0%" /></p>
<div class="center">
<img src="./figures/loss_depth_2.png"" style="width:80.0%" />
</div>
<div class="center">
<img src="./figures/loss_depth_4.png"" style="width:80.0%" />
</div>
<div class="center">
<img src="./figures/loss_depth_6.png"" style="width:80.0%" />
</div>
<div class="center">
<img src="./figures/loss_depth_8.png"" style="width:80.0%" />
</div>
<p><u><strong>2. Stochastic gradient noise:</strong></u></p>
<img src="./figures/heavy_tail_noise_depth_2.png"" style="width:70.0%" />
<img src="./figures/heavy_tail_noise_depth_4.png"" style="width:70.0%" />
<img src="./figures/heavy_tail_noise_depth_6.png"" style="width:70.0%" />
<img src="./figures/heavy_tail_noise_depth_8.png"" style="width:70.0%" />
<p><u><strong>3. Robust condition number:</strong></u></p>
<img src="./figures/condition_number_depth_2.png"" style="width:70.0%" />
<img src="./figures/condition_number_depth_4.png"" style="width:70.0%" />
<img src="./figures/condition_number_depth_6.png"" style="width:70.0%" />
<img src="./figures/condition_number_depth_8.png"" style="width:70.0%" />
</div>
<figcaption>Comparing the robust condition number for different number of layers.</figcaption>
</figure>

## Effect of more layers

We investigate the effect of the number of layers $`L`$ on the optimization. Specifically,

<div class="center">

***Q.** Will a deeper linear transformer exacerbate the features in <a href="#sec:features" data-reference-type="ref+label" data-reference="sec:features">2</a>?*

</div>

**Settings.** In order to investigate the above question, we consider repeating the experiments in <a href="#sec:linear_features" data-reference-type="ref+label" data-reference="sec:linear_features">3.2</a> for the number of layers $`L\in\{2,4,6,8\}`$.

**Discussion.** We present the experimental results presented in Figures <a href="#fig:sgdadam_3" data-reference-type="ref" data-reference="fig:sgdadam_3">[fig:sgdadam_3]</a>, <a href="#fig:histogram_3" data-reference-type="ref" data-reference="fig:histogram_3">[fig:histogram_3]</a>, and <a href="#fig:robust_3" data-reference-type="ref" data-reference="fig:robust_3">8</a>.

- As one can see from <a href="#fig:sgdadam_3" data-reference-type="ref+label" data-reference="fig:sgdadam_3">[fig:sgdadam_3]</a>, the gap in loss between adaptive methods and SGD become more and more pronounced as we increase the number of layers.

- On the other hand, the absolute value of the loss decreases with increasing depth, for both SGD and Adam, which makes sense considering the larger capacity of deeper models.

- We plot the stochastic gradient noise for different settings in <a href="#fig:histogram_3" data-reference-type="ref+label" data-reference="fig:histogram_3">[fig:histogram_3]</a>. We do see that the noise for the case of $`L=6,8`$ are more heavy-tailed than the case of $`L=2,4`$. In particular, the noise distribution for $`L=2`$ is much less heavy-tailed than that for $`L=8`$.

- Lastly, we observe in <a href="#fig:robust_3" data-reference-type="ref+label" data-reference="fig:robust_3">8</a> that the gap in the robust condition number of SGD and Adam is more pronounced in deeper models ($`L = 4,6,8`$) than the shallow model ($`L=2`$).

# Conclusion

The complexity of modern neural networks, especially transformers, often eludes precise mathematical understanding, and hence calls for such “physics-style” approaches (c.f. ) based on simplified models. This work presents a concrete addition to this viewpoint, and it builds a valuable, realistic proxy for understanding transformers. We hope that our work will serve as the stepping stone for building a more precise theory of transformer optimization, as well as contributing to the development of efficient training methods for transformers.

# Acknowledgements

This work stems from a group project at MIT; we thank the collaborators in the group, Hadi Daneshmand, Haochuan Li, Zakaria Mhammedi, Swati Padmanabhan, Amirhossein Reisizadeh, and William Wang for their time and intriguing discussions.

Kwangjun Ahn and Ali Jadbabaie were supported by the ONR grant (N00014-23-1-2299) and MIT-IBM Watson as well as a Vannevar Bush fellowship from Office of the Secretary of Defense. Xiang Cheng and Suvrit Sra acknowledge support from NSF CCF-2112665 (TILOS AI Research Institute) and an NSF CAREER award (1846088). Minhak Song and Chulhee Yun were supported by Institute of Information & communications Technology Planning & Evaluation (IITP) grant (No. 2019-0-00075, Artificial Intelligence Graduate School Program (KAIST)) funded by the Korea government (MSIT), two National Research Foundation of Korea (NRF) grants (No. NRF-2019R1A5A1028324, RS-2023-00211352) funded by the Korea government (MSIT), and a grant funded by Samsung Electronics Co., Ltd.

# References

<div class="thebibliography">

Jacob Abernethy, Alekh Agarwal, Teodor V Marinov, and Manfred K Warmuth A mechanism for sample-efficient in-context learning for sparse retrieval tasks *arXiv preprint arXiv:2305.17040*, 2023. **Abstract:** We study the phenomenon of \\}textit{in-context learning} (ICL) exhibited by large language models, where they can adapt to a new learning task, given a handful of labeled examples, without any explicit parameter optimization. Our goal is to explain how a pre-trained transformer model is able to perform ICL under reasonable assumptions on the pre-training process and the downstream tasks. We posit a mechanism whereby a transformer can achieve the following: (a) receive an i.i.d. sequence of examples which have been converted into a prompt using potentially-ambiguous delimiters, (b) correctly segment the prompt into examples and labels, (c) infer from the data a \\}textit{sparse linear regressor} hypothesis, and finally (d) apply this hypothesis on the given test example and return a predicted label. We establish that this entire procedure is implementable using the transformer mechanism, and we give sample complexity guarantees for this learning framework. Our empirical findings validate the challenge of segmentation, and we show a correspondence between our posited mechanisms and observed attention maps for step (c). (@abernethy2023mechanism)

Kwangjun Ahn, Sébastien Bubeck, Sinho Chewi, Yin Tat Lee, Felipe Suarez, and Yi Zhang Learning threshold neurons via the "edge of stability" *NeurIPS 2023 (arXiv:2212.07469)*, 2023. **Abstract:** Existing analyses of neural network training often operate under the unrealistic assumption of an extremely small learning rate. This lies in stark contrast to practical wisdom and empirical studies, such as the work of J. Cohen et al. (ICLR 2021), which exhibit startling new phenomena (the "edge of stability" or "unstable convergence") and potential benefits for generalization in the large learning rate regime. Despite a flurry of recent works on this topic, however, the latter effect is still poorly understood. In this paper, we take a step towards understanding genuinely non-convex training dynamics with large learning rates by performing a detailed analysis of gradient descent for simplified models of two-layer neural networks. For these models, we provably establish the edge of stability phenomenon and discover a sharp phase transition for the step size below which the neural network fails to learn "threshold-like" neurons (i.e., neurons with a non-zero first-layer bias). This elucidates one possible mechanism by which the edge of stability can in fact lead to better generalization, as threshold neurons are basic building blocks with useful inductive bias for many tasks. (@ahn2022learning)

Kwangjun Ahn, Xiang Cheng, Hadi Daneshmand, and Suvrit Sra Transformers learn to implement preconditioned gradient descent for in-context learning *NeurIPS 2023 (arXiv:2306.00297)*, 2023. **Abstract:** Several recent works demonstrate that transformers can implement algorithms like gradient descent. By a careful construction of weights, these works show that multiple layers of transformers are expressive enough to simulate iterations of gradient descent. Going beyond the question of expressivity, we ask: Can transformers learn to implement such algorithms by training over random problem instances? To our knowledge, we make the first theoretical progress on this question via an analysis of the loss landscape for linear transformers trained over random instances of linear regression. For a single attention layer, we prove the global minimum of the training objective implements a single iteration of preconditioned gradient descent. Notably, the preconditioning matrix not only adapts to the input distribution but also to the variance induced by data inadequacy. For a transformer with $L$ attention layers, we prove certain critical points of the training objective implement $L$ iterations of preconditioned gradient descent. Our results call for future theoretical studies on learning algorithms by training transformers. (@ahn2023transformers)

Ekin Akyürek, Dale Schuurmans, Jacob Andreas, Tengyu Ma, and Denny Zhou What learning algorithm is in-context learning? investigations with linear models *International Conference on Learning Representations*, 2022. **Abstract:** Neural sequence models, especially transformers, exhibit a remarkable capacity for in-context learning. They can construct new predictors from sequences of labeled examples $(x, f(x))$ presented in the input without further parameter updates. We investigate the hypothesis that transformer-based in-context learners implement standard learning algorithms implicitly, by encoding smaller models in their activations, and updating these implicit models as new examples appear in the context. Using linear regression as a prototypical problem, we offer three sources of evidence for this hypothesis. First, we prove by construction that transformers can implement learning algorithms for linear models based on gradient descent and closed-form ridge regression. Second, we show that trained in-context learners closely match the predictors computed by gradient descent, ridge regression, and exact least-squares regression, transitioning between different predictors as transformer depth and dataset noise vary, and converging to Bayesian estimators for large widths and depths. Third, we present preliminary evidence that in-context learners share algorithmic features with these predictors: learners’ late layers non-linearly encode weight vectors and moment matrices. These results suggest that in-context learning is understandable in algorithmic terms, and that (at least in the linear case) learners may rediscover standard estimation algorithms. Code and reference implementations are released at https://github.com/ekinakyurek/google-research/blob/master/incontext. (@akyurek2022learning)

Zeyuan Allen-Zhu and Yuanzhi Li Physics of language models: Part 1, context-free grammar *arXiv preprint arXiv:2305.13673*, 2023. **Abstract:** Transformer-based language models are effective but complex, and understanding their inner workings and reasoning mechanisms is a significant challenge. Previous research has primarily explored how these models handle simple tasks like name copying or selection, and we extend this by investigating how these models perform recursive language structure reasoning defined by context-free grammars (CFGs). We introduce a family of synthetic CFGs that produce hierarchical rules, capable of generating lengthy sentences (e.g., hundreds of tokens) that are locally ambiguous and require dynamic programming to parse. Despite this complexity, we demonstrate that generative models like GPT can accurately learn and reason over CFG-defined hierarchies and generate sentences based on it. We explore the model’s internals, revealing that its hidden states precisely capture the structure of CFGs, and its attention patterns resemble the information passing in a dynamic programming algorithm. This paper also presents several corollaries, including showing why absolute positional embeddings is inferior to relative and rotary embeddings; uniform attention alone is surprisingly effective (motivating our follow-up work on Canon layers); encoder-only models (e.g., BERT, DeBERTa) struggle with deep structure reasoning on CFGs compared to autoregressive models (e.g., GPT); and injecting structural or syntactic noise into pretraining data markedly improves robustness to corrupted language prompts. (@allen2023physics)

Sébastien Bubeck Convex optimization: Algorithms and complexity *Foundations and Trends® in Machine Learning*, 8 (3-4): 231–357, 2015. **Abstract:** This monograph presents the main complexity theorems in convex optimization and their corresponding algorithms. Starting from the fundamental theory of black-box optimization, the material progresses towards recent advances in structural optimization and stochastic optimization. Our presentation of black-box optimization, strongly influenced by the seminal book of Nesterov, includes the analysis of cutting plane methods, as well as accelerated gradient descent schemes. We also pay special attention to non-Euclidean settings relevant algorithms include Frank-Wolfe, mirror descent, and dual averaging and discuss their relevance in machine learning. We provide a gentle introduction to structural optimization with FISTA to optimize a sum of a smooth and a simple non-smooth term, saddle-point mirror prox Nemirovski’s alternative to Nesterov’s smoothing, and a concise description of interior point methods. In stochastic optimization we discuss stochastic gradient descent, mini-batches, random coordinate descent, and sublinear algorithms. We also briefly touch upon convex relaxation of combinatorial problems and the use of randomness to round solutions, as well as random walks based methods. (@bubeck2015convex)

Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, et al Sparks of artificial general intelligence: Early experiments with gpt-4 *arXiv preprint arXiv:2303.12712*, 2023. **Abstract:** Artificial intelligence (AI) researchers have been developing and refining large language models (LLMs) that exhibit remarkable capabilities across a variety of domains and tasks, challenging our understanding of learning and cognition. The latest model developed by OpenAI, GPT-4, was trained using an unprecedented scale of compute and data. In this paper, we report on our investigation of an early version of GPT-4, when it was still in active development by OpenAI. We contend that (this early version of) GPT-4 is part of a new cohort of LLMs (along with ChatGPT and Google’s PaLM for example) that exhibit more general intelligence than previous AI models. We discuss the rising capabilities and implications of these models. We demonstrate that, beyond its mastery of language, GPT-4 can solve novel and difficult tasks that span mathematics, coding, vision, medicine, law, psychology and more, without needing any special prompting. Moreover, in all of these tasks, GPT-4’s performance is strikingly close to human-level performance, and often vastly surpasses prior models such as ChatGPT. Given the breadth and depth of GPT-4’s capabilities, we believe that it could reasonably be viewed as an early (yet still incomplete) version of an artificial general intelligence (AGI) system. In our exploration of GPT-4, we put special emphasis on discovering its limitations, and we discuss the challenges ahead for advancing towards deeper and more comprehensive versions of AGI, including the possible need for pursuing a new paradigm that moves beyond next-word prediction. We conclude with reflections on societal influences of the recent technological leap and future research directions. (@bubeck2023sparks)

Michael Crawshaw, Mingrui Liu, Francesco Orabona, Wei Zhang, and Zhenxun Zhuang Robustness to unbounded smoothness of generalized signsgd *Advances in Neural Information Processing Systems*, 35: 9955–9968, 2022. **Abstract:** Traditional analyses in non-convex optimization typically rely on the smoothness assumption, namely requiring the gradients to be Lipschitz. However, recent evidence shows that this smoothness condition does not capture the properties of some deep learning objective functions, including the ones involving Recurrent Neural Networks and LSTMs. Instead, they satisfy a much more relaxed condition, with potentially unbounded smoothness. Under this relaxed assumption, it has been theoretically and empirically shown that the gradient-clipped SGD has an advantage over the vanilla one. In this paper, we show that clipping is not indispensable for Adam-type algorithms in tackling such scenarios: we theoretically prove that a generalized SignSGD algorithm can obtain similar convergence rates as SGD with clipping but does not need explicit clipping at all. This family of algorithms on one end recovers SignSGD and on the other end closely resembles the popular Adam algorithm. Our analysis underlines the critical role that momentum plays in analyzing SignSGD-type and Adam-type algorithms: it not only reduces the effects of noise, thus removing the need for large mini-batch in previous analyses of SignSGD-type algorithms, but it also substantially reduces the effects of unbounded smoothness and gradient norms. We also compare these algorithms with popular optimizers on a set of deep learning tasks, observing that we can match the performance of Adam while beating the others. (@crawshaw2022robustness)

Yan Dai, Kwangjun Ahn, and Suvrit Sra The crucial role of normalization in sharpness-aware minimization *NeurIPS 2023 (arXiv:2305.15287)*, 2023. **Abstract:** Sharpness-Aware Minimization (SAM) is a recently proposed gradient-based optimizer (Foret et al., ICLR 2021) that greatly improves the prediction performance of deep neural networks. Consequently, there has been a surge of interest in explaining its empirical success. We focus, in particular, on understanding the role played by normalization, a key component of the SAM updates. We theoretically and empirically study the effect of normalization in SAM for both convex and non-convex functions, revealing two key roles played by normalization: i) it helps in stabilizing the algorithm; and ii) it enables the algorithm to drift along a continuum (manifold) of minima – a property identified by recent theoretical works that is the key to better performance. We further argue that these two properties of normalization make SAM robust against the choice of hyper-parameters, supporting the practicality of SAM. Our conclusions are backed by various experiments. (@dai2023crucial)

J Devlin, MW Chang, K Lee, and K Toutanova Bert: Pre-training of deep bidirectional transformers for language understanding in: Proceedings of the 2019 conference of the north american chapter of the association for computational linguistics, 4171–4186.. acl. *ACL. DOI: https://doi. org/10.18653/v1*, (19): 1423, 2019. **Abstract:** We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5 (7.7 point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement). (@devlin2018bert)

Shivam Garg, Dimitris Tsipras, Percy S Liang, and Gregory Valiant What can transformers learn in-context? a case study of simple function classes *Advances in Neural Information Processing Systems*, 35: 30583–30598, 2022. **Abstract:** In-context learning refers to the ability of a model to condition on a prompt sequence consisting of in-context examples (input-output pairs corresponding to some task) along with a new query input, and generate the corresponding output. Crucially, in-context learning happens only at inference time without any parameter updates to the model. While large language models such as GPT-3 exhibit some ability to perform in-context learning, it is unclear what the relationship is between tasks on which this succeeds and what is present in the training data. To make progress towards understanding in-context learning, we consider the well-defined problem of training a model to in-context learn a function class (e.g., linear functions): that is, given data derived from some functions in the class, can we train a model to in-context learn "most" functions from this class? We show empirically that standard Transformers can be trained from scratch to perform in-context learning of linear functions – that is, the trained model is able to learn unseen linear functions from in-context examples with performance comparable to the optimal least squares estimator. In fact, in-context learning is possible even under two forms of distribution shift: (i) between the training data of the model and inference-time prompts, and (ii) between the in-context examples and the query input during inference. We also show that we can train Transformers to in-context learn more complex function classes – namely sparse linear functions, two-layer neural networks, and decision trees – with performance that matches or exceeds task-specific learning algorithms. Our code and models are available at https://github.com/dtsip/in-context-learning . (@garg2022can)

Kaiqi Jiang, Dhruv Malik, and Yuanzhi Li How does adaptive optimization impact local neural network geometry? *arXiv preprint arXiv:2211.02254*, 2022. **Abstract:** Adaptive optimization methods are well known to achieve superior convergence relative to vanilla gradient methods. The traditional viewpoint in optimization, particularly in convex optimization, explains this improved performance by arguing that, unlike vanilla gradient schemes, adaptive algorithms mimic the behavior of a second-order method by adapting to the global geometry of the loss function. We argue that in the context of neural network optimization, this traditional viewpoint is insufficient. Instead, we advocate for a local trajectory analysis. For iterate trajectories produced by running a generic optimization algorithm OPT, we introduce $R^{\\}text{OPT}}\_{\\}text{med}}$, a statistic that is analogous to the condition number of the loss Hessian evaluated at the iterates. Through extensive experiments, we show that adaptive methods such as Adam bias the trajectories towards regions where $R^{\\}text{Adam}}\_{\\}text{med}}$ is small, where one might expect faster convergence. By contrast, vanilla gradient methods like SGD bias the trajectories towards regions where $R^{\\}text{SGD}}\_{\\}text{med}}$ is comparatively large. We complement these empirical observations with a theoretical result that provably demonstrates this phenomenon in the simplified setting of a two-layer linear network. We view our findings as evidence for the need of a new explanation of the success of adaptive methods, one that is different than the conventional wisdom. (@jiang2022does)

Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei Scaling laws for neural language models *arXiv preprint arXiv:2001.08361*, 2020. **Abstract:** We study empirical scaling laws for language model performance on the cross-entropy loss. The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude. Other architectural details such as network width or depth have minimal effects within a wide range. Simple equations govern the dependence of overfitting on model/dataset size and the dependence of training speed on model size. These relationships allow us to determine the optimal allocation of a fixed compute budget. Larger models are significantly more sample-efficient, such that optimally compute-efficient training involves training very large models on a relatively modest amount of data and stopping significantly before convergence. (@kaplan2020scaling)

Frederik Kunstner, Jacques Chen, Jonathan Wilder Lavington, and Mark Schmidt Noise is not the main factor behind the gap between sgd and adam on transformers, but sign descent might be *In International Conference on Learning Representations (ICLR) (arXiv:2304.13960)*, 2023. **Abstract:** The success of the Adam optimizer on a wide array of architectures has made it the default in settings where stochastic gradient descent (SGD) performs poorly. However, our theoretical understanding of this discrepancy is lagging, preventing the development of significant improvements on either algorithm. Recent work advances the hypothesis that Adam and other heuristics like gradient clipping outperform SGD on language tasks because the distribution of the error induced by sampling has heavy tails. This suggests that Adam outperform SGD because it uses a more robust gradient estimate. We evaluate this hypothesis by varying the batch size, up to the entire dataset, to control for stochasticity. We present evidence that stochasticity and heavy-tailed noise are not major factors in the performance gap between SGD and Adam. Rather, Adam performs better as the batch size increases, while SGD is less effective at taking advantage of the reduction in noise. This raises the question as to why Adam outperforms SGD in the full-batch setting. Through further investigation of simpler variants of SGD, we find that the behavior of Adam with large batches is similar to sign descent with momentum. (@kunstner2023noise)

Yuchen Li, Yuanzhi Li, and Andrej Risteski How do transformers learn topic structure: Towards a mechanistic understanding *International Conference on Machine Learning (ICML) (arXiv:2303.04245)*, 2023. **Abstract:** While the successes of transformers across many domains are indisputable, accurate understanding of the learning mechanics is still largely lacking. Their capabilities have been probed on benchmarks which include a variety of structured and reasoning tasks – but mathematical understanding is lagging substantially behind. Recent lines of work have begun studying representational aspects of this question: that is, the size/depth/complexity of attention-based networks to perform certain tasks. However, there is no guarantee the learning dynamics will converge to the constructions proposed. In our paper, we provide fine-grained mechanistic understanding of how transformers learn "semantic structure", understood as capturing co-occurrence structure of words. Precisely, we show, through a combination of mathematical analysis and experiments on Wikipedia data and synthetic data modeled by Latent Dirichlet Allocation (LDA), that the embedding layer and the self-attention layer encode the topical structure. In the former case, this manifests as higher average inner product of embeddings between same-topic words. In the latter, it manifests as higher average pairwise attention between same-topic words. The mathematical results involve several assumptions to make the analysis tractable, which we verify on data, and might be of independent interest as well. (@li2023transformers)

Liyuan Liu, Xiaodong Liu, Jianfeng Gao, Weizhu Chen, and Jiawei Han Understanding the difficulty of training transformers In *2020 Conference on Empirical Methods in Natural Language Processing, EMNLP 2020*, pages 5747–5763. Association for Computational Linguistics (ACL), 2020. **Abstract:** Transformers have proved effective in many NLP tasks. However, their training requires non-trivial efforts regarding carefully designing cutting-edge optimizers and learning rate schedulers (e.g., conventional SGD fails to train Transformers effectively). Our objective here is to understand \_\_what complicates Transformer training\_\_ from both empirical and theoretical perspectives. Our analysis reveals that unbalanced gradients are not the root cause of the instability of training. Instead, we identify an amplification effect that influences training substantially—for each layer in a multi-layer Transformer model, heavy dependency on its residual branch makes training unstable, since it amplifies small parameter perturbations (e.g., parameter updates) and results in significant disturbances in the model output. Yet we observe that a light dependency limits the model potential and leads to inferior trained models. Inspired by our analysis, we propose Admin (Adaptive model initialization) to stabilize the early stage’s training and unleash its full potential in the late stage. Extensive experiments show that Admin is more stable, converges faster, and leads to better performance (@liu2020understanding)

Arvind Mahankali, Tatsunori B Hashimoto, and Tengyu Ma One step of gradient descent is provably the optimal in-context learner with one layer of linear self-attention *arXiv preprint arXiv:2307.03576*, 2023. **Abstract:** Recent works have empirically analyzed in-context learning and shown that transformers trained on synthetic linear regression tasks can learn to implement ridge regression, which is the Bayes-optimal predictor, given sufficient capacity \[Aky\\}"urek et al., 2023\], while one-layer transformers with linear self-attention and no MLP layer will learn to implement one step of gradient descent (GD) on a least-squares linear regression objective \[von Oswald et al., 2022\]. However, the theory behind these observations remains poorly understood. We theoretically study transformers with a single layer of linear self-attention, trained on synthetic noisy linear regression data. First, we mathematically show that when the covariates are drawn from a standard Gaussian distribution, the one-layer transformer which minimizes the pre-training loss will implement a single step of GD on the least-squares linear regression objective. Then, we find that changing the distribution of the covariates and weight vector to a non-isotropic Gaussian distribution has a strong impact on the learned algorithm: the global minimizer of the pre-training loss now implements a single step of $\\}textit{pre-conditioned}$ GD. However, if only the distribution of the responses is changed, then this does not have a large effect on the learned algorithm: even when the response comes from a more general family of $\\}textit{nonlinear}$ functions, the global minimizer of the pre-training loss still implements a single step of GD on a least-squares linear regression objective. (@mahankali2023one)

Yurii Nesterov *Lectures on convex optimization*, volume 137 Springer, 2018. (@Nesterov2018)

Yan Pan and Yuanzhi Li Toward understanding why adam converges faster than sgd for transformers *arXiv preprint arXiv:2306.00204*, 2023. **Abstract:** While stochastic gradient descent (SGD) is still the most popular optimization algorithm in deep learning, adaptive algorithms such as Adam have established empirical advantages over SGD in some deep learning applications such as training transformers. However, it remains a question that why Adam converges significantly faster than SGD in these scenarios. In this paper, we propose one explanation of why Adam converges faster than SGD using a new concept directional sharpness. We argue that the performance of optimization algorithms is closely related to the directional sharpness of the update steps, and show SGD has much worse directional sharpness compared to adaptive algorithms. We further observe that only a small fraction of the coordinates causes the bad sharpness and slow convergence of SGD, and propose to use coordinate-wise clipping as a solution to SGD and other optimization algorithms. We demonstrate the effect of coordinate-wise clipping on sharpness reduction and speeding up the convergence of optimization algorithms under various settings. We show that coordinate-wise clipping improves the local loss reduction when only a small fraction of the coordinates has bad sharpness. We conclude that the sharpness reduction effect of adaptive coordinate-wise scaling is the reason for Adam’s success in practice and suggest the use of coordinate-wise clipping as a universal technique to speed up deep learning optimization. (@pan2023toward)

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin Attention is all you need *Advances in neural information processing systems*, 2017. **Abstract:** The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data. (@vaswani2017attention)

Johannes von Oswald, Eyvind Niklasson, Ettore Randazzo, João Sacramento, Alexander Mordvintsev, Andrey Zhmoginov, and Max Vladymyrov Transformers learn in-context by gradient descent In *International Conference on Machine Learning*, pages 35151–35174. PMLR, 2023. **Abstract:** At present, the mechanisms of in-context learning in Transformers are not well understood and remain mostly an intuition. In this paper, we suggest that training Transformers on auto-regressive objectives is closely related to gradient-based meta-learning formulations. We start by providing a simple weight construction that shows the equivalence of data transformations induced by 1) a single linear self-attention layer and by 2) gradient-descent (GD) on a regression loss. Motivated by that construction, we show empirically that when training self-attention-only Transformers on simple regression tasks either the models learned by GD and Transformers show great similarity or, remarkably, the weights found by optimization match the construction. Thus we show how trained Transformers become mesa-optimizers i.e. learn models by gradient descent in their forward pass. This allows us, at least in the domain of regression problems, to mechanistically understand the inner workings of in-context learning in optimized Transformers. Building on this insight, we furthermore identify how Transformers surpass the performance of plain gradient descent by learning an iterative curvature correction and learn linear models on deep data representations to solve non-linear regression tasks. Finally, we discuss intriguing parallels to a mechanism identified to be crucial for in-context learning termed induction-head (Olsson et al., 2022) and show how it could be understood as a specific case of in-context learning by gradient descent learning within Transformers. Code to reproduce the experiments can be found at https://github.com/google-research/self-organising-systems/tree/master/transformers_learn_icl_by_gd . (@von2022transformers)

Ashia C Wilson, Rebecca Roelofs, Mitchell Stern, Nati Srebro, and Benjamin Recht The marginal value of adaptive gradient methods in machine learning In *Advances in Neural Information Processing Systems*, pages 4148–4158, 2017. **Abstract:** Adaptive optimization methods, which perform local optimization with a metric constructed from the history of iterates, are becoming increasingly popular for training deep neural networks. Examples include AdaGrad, RMSProp, and Adam. We show that for simple overparameterized problems, adaptive methods often find drastically different solutions than gradient descent (GD) or stochastic gradient descent (SGD). We construct an illustrative binary classification problem where the data is linearly separable, GD and SGD achieve zero test error, and AdaGrad, Adam, and RMSProp attain test errors arbitrarily close to half. We additionally study the empirical generalization capability of adaptive methods on several state-of-the-art deep learning models. We observe that the solutions found by adaptive methods generalize worse (often significantly worse) than SGD, even when these solutions have better training performance. These results suggest that practitioners should reconsider the use of adaptive methods to train neural networks. (@wilson2017marginal)

Jingzhao Zhang, Tianxing He, Suvrit Sra, and Ali Jadbabaie Why gradient clipping accelerates training: A theoretical justification for adaptivity In *International Conference on Learning Representations (ICLR)*, 2020. **Abstract:** We provide a theoretical explanation for the effectiveness of gradient clipping in training deep neural networks. The key ingredient is a new smoothness condition derived from practical neural network training examples. We observe that gradient smoothness, a concept central to the analysis of first-order optimization algorithms that is often assumed to be a constant, demonstrates significant variability along the training trajectory of deep neural networks. Further, this smoothness positively correlates with the gradient norm, and contrary to standard assumptions in the literature, it can grow with the norm of the gradient. These empirical observations limit the applicability of existing theoretical analyses of algorithms that rely on a fixed bound on smoothness. These observations motivate us to introduce a novel relaxation of gradient smoothness that is weaker than the commonly used Lipschitz smoothness assumption. Under the new condition, we prove that two popular methods, namely, \\}emph{gradient clipping} and \\}emph{normalized gradient}, converge arbitrarily faster than gradient descent with fixed stepsize. We further explain why such adaptively scaled gradient methods can accelerate empirical convergence and verify our results empirically in popular neural network training settings. (@zhang2019gradient)

Jingzhao Zhang, Sai Praneeth Karimireddy, Andreas Veit, Seungyeon Kim, Sashank Reddi, Sanjiv Kumar, and Suvrit Sra Why are adaptive methods good for attention models? *Advances in Neural Information Processing Systems*, 33: 15383–15393, 2020. **Abstract:** While stochastic gradient descent (SGD) is still the \\}emph{de facto} algorithm in deep learning, adaptive methods like Clipped SGD/Adam have been observed to outperform SGD across important tasks, such as attention models. The settings under which SGD performs poorly in comparison to adaptive methods are not well understood yet. In this paper, we provide empirical and theoretical evidence that a heavy-tailed distribution of the noise in stochastic gradients is one cause of SGD’s poor performance. We provide the first tight upper and lower convergence bounds for adaptive gradient methods under heavy-tailed noise. Further, we demonstrate how gradient clipping plays a key role in addressing heavy-tailed gradient noise. Subsequently, we show how clipping can be applied in practice by developing an \\}emph{adaptive} coordinate-wise clipping algorithm (ACClip) and demonstrate its superior performance on BERT pretraining and finetuning tasks. (@zhang2020adaptive)

Ruiqi Zhang, Spencer Frei, and Peter L Bartlett Trained transformers learn linear models in-context *arXiv preprint arXiv:2306.09927*, 2023. **Abstract:** Attention-based neural networks such as transformers have demonstrated a remarkable ability to exhibit in-context learning (ICL): Given a short prompt sequence of tokens from an unseen task, they can formulate relevant per-token and next-token predictions without any parameter updates. By embedding a sequence of labeled training data and unlabeled test data as a prompt, this allows for transformers to behave like supervised learning algorithms. Indeed, recent work has shown that when training transformer architectures over random instances of linear regression problems, these models’ predictions mimic those of ordinary least squares. Towards understanding the mechanisms underlying this phenomenon, we investigate the dynamics of ICL in transformers with a single linear self-attention layer trained by gradient flow on linear regression tasks. We show that despite non-convexity, gradient flow with a suitable random initialization finds a global minimum of the objective function. At this global minimum, when given a test prompt of labeled examples from a new prediction task, the transformer achieves prediction error competitive with the best linear predictor over the test prompt distribution. We additionally characterize the robustness of the trained transformer to a variety of distribution shifts and show that although a number of shifts are tolerated, shifts in the covariate distribution of the prompts are not. Motivated by this, we consider a generalized ICL setting where the covariate distributions can vary across prompts. We show that although gradient flow succeeds at finding a global minimum in this setting, the trained transformer is still brittle under mild covariate shifts. We complement this finding with experiments on large, nonlinear transformer architectures which we show are more robust under covariate shifts. (@zhang2023trained)

Yi Zhang, Arturs Backurs, Sébastien Bubeck, Ronen Eldan, Suriya Gunasekar, and Tal Wagner Unveiling transformers with lego: a synthetic reasoning task *arXiv preprint arXiv:2206.04301*, 2022. **Abstract:** We propose a synthetic reasoning task, LEGO (Learning Equality and Group Operations), that encapsulates the problem of following a chain of reasoning, and we study how the Transformer architectures learn this task. We pay special attention to data effects such as pretraining (on seemingly unrelated NLP tasks) and dataset composition (e.g., differing chain length at training and test time), as well as architectural variants such as weight-tied layers or adding convolutional components. We study how the trained models eventually succeed at the task, and in particular, we manage to understand some of the attention heads as well as how the information flows in the network. In particular, we have identified a novel \\}emph{association} pattern that globally attends only to identical tokens. Based on these observations we propose a hypothesis that here pretraining helps for LEGO tasks due to certain structured attention patterns, and we experimentally verify this hypothesis. We also observe that in some data regime the trained transformer finds “shortcut" solutions to follow the chain of reasoning, which impedes the model’s robustness, and moreover we propose ways to prevent it. Motivated by our findings on structured attention patterns, we propose the LEGO attention module, a drop-in replacement for vanilla attention heads. This architectural change significantly reduces Flops and maintains or even \\}emph{improves} the model’s performance at large-scale pretraining. (@zhang2022unveiling)

</div>

[^1]: In fact, in their paper, they instead consider the maximum diagonal entry of the Hessian divided by the median diagonal entry as an approximation of this quantity.

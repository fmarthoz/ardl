import numpy as np

def binary_budget(T, budget=50000,p1=.9,p2=.08,seed=0):
    rng=np.random.default_rng(seed)
    z=np.zeros(T, dtype=int)
    z[0]=rng.integers(0,2)
    for t in range(1,T):
        z[t]=int(rng.random()<(p1 if z[t-1] else p2))
    spend=budget*z
    return spend, z


def mean_reverting_budget(T=104,mu=20000,cap=None, seed=0,phi=.8,sigma=1000):
    rng=np.random.default_rng(seed)
    z=np.zeros(T, dtype=int)
    z[0]=mu+rng.normal(0,sigma)
    for t in range(1,T):
        r=rng.normal(0,sigma)
        z[t]=mu+phi*(z[t-1]-mu)+r
    if cap:
        return np.minimum(cap,z)
    else:
        return(z)


def generate_sales_data_old(*series, betas, intercept=0.0, eps=1e-12):
    X = np.column_stack([np.asarray(s, float).reshape(-1) for s in series])
    beta = np.asarray(betas, float).reshape(-1)
    if X.shape[1] != beta.size:
        raise ValueError("Number of series must match number of betas.")
    # y = exp(intercept) * prod_i x_i**beta_i
    return np.exp(intercept) * np.prod((1+X + eps) ** beta, axis=1)

def generate_sales_data(*series, betas, intercept=0.0, iterations=5, eps=0.2):
    T=len(series[0])
    matr=np.column_stack(np.log1p(series))
    ar=matr@betas[:-1]
    matr=np.column_stack([matr,ar])
    for i in range(iterations):
        ln_sales=matr@betas+intercept
        matr[:,-1]=np.roll(ln_sales,1)
    # add noise at the end
    noise=np.random.normal(0, eps,T)
    return np.exp(ln_sales+noise)


#print(generate_sales_data([50000,5000,50000],[20125,19980,20622],[50000,49916,50000],betas=[0.005,0.15,.14,.5],intercept=3,iterations=50,eps=0.1))

def add_seasonality(x,cycles=3,h=0.1):
    v = np.linspace(0, cycles*2*np.pi, len(x))
    y = h*np.sin(v)
    sales=x*(y+1)
    return sales
    
def add_adstock(x,l):
    if l>=1 or l<=0:
        print("ERROR:lambda must be between 0 and 1")
        return 0
    T=len(x)
    sales=np.zeros(T)
    sales[0]=x[0]
    for i in range(1,T):
        sales[i]=sales[i-1]*l+x[i]
    return sales

def add_trend(x,p=0.10):
    x=np.array(x)
    T=len(x)
    m=range(T)
    m=m*(x[T-1]*(1+p)-x[T-1])/T
    return m+x

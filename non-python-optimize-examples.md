# JS & JSX Examples

## Example 1:

### Code Snippet:
```
const AppLoaderComponent = (props) => {
  const params = useParams();
  const appId = params.id;

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => loadAppDetails(), []);

  const loadAppDetails = () => {
    appService.getApp(appId, 'edit').catch((error) => {
      handleError(error);
    });
  };

  const switchOrganization = (orgId) => {
    const path = `/apps/${appId}`;
    const sub_path = window?.public_config?.SUB_PATH ? stripTrailingSlash(window?.public_config?.SUB_PATH) : '';
    organizationService.switchOrganization(orgId).then(
      () => {
        window.location.href = `${sub_path}/${orgId}${path}`;
      },
      () => {
        return (window.location.href = `${sub_path}/login/${orgId}?redirectTo=${path}`);
      }
    );
  };

  const handleError = (error) => {
    try {
      if (error?.data) {
        const statusCode = error.data?.statusCode;
        if (statusCode === 403) {
          const errorObj = safelyParseJSON(error.data?.message);
          if (
            errorObj?.organizationId &&
            authenticationService.currentSessionValue.current_organization_id !== errorObj?.organizationId
          ) {
            switchOrganization(errorObj?.organizationId);
            return;
          }
          redirectToDashboard();
        } else if (statusCode === 401) {
          window.location = `${getSubpath() ?? ''}/login${
            !_.isEmpty(getWorkspaceId()) ? `/${getWorkspaceId()}` : ''
          }?redirectTo=${this.props.location.pathname}`;
          return;
        } else if (statusCode === 404 || statusCode === 422) {
          toast.error(error?.error ?? 'App not found');
        }
        redirectToDashboard();
      }
    } catch (err) {
      redirectToDashboard();
    }
  };

  return config.ENABLE_MULTIPLAYER_EDITING ? <RealtimeEditor {...props} /> : <Editor {...props} />;
};

export const AppLoader = withTranslation()(AppLoaderComponent);
```
### Result
```
Brief description of the current performance limitation or bottleneck.
The current code has a few performance limitations. Firstly, the useEffect hook is used to call loadAppDetails function, but the dependency array is empty, which means it will only run once after the initial render. If appId changes, the loadAppDetails function will not be called again. Secondly, the loadAppDetails and handleError functions are defined inside the component, which means they will be redefined on every render. Lastly, the switchOrganization function creates a new promise every time it's called, which can be avoided.

Improvement steps:

Move the loadAppDetails and handleError functions outside of the component and pass necessary arguments to them. This will prevent unnecessary redefinition of these functions on every render.
Use the useCallback hook for the switchOrganization function to avoid creating a new function on every render.
Add appId to the dependency array of the useEffect hook to ensure that the loadAppDetails function is called whenever appId changes.
Improved code:

const loadAppDetails = (appId) => {
  appService.getApp(appId, 'edit').catch((error) => {
    handleError(error, appId);
  });
};

const handleError = (error, appId) => {
  // ... same code as before ...
};

const AppLoaderComponent = (props) => {
  const params = useParams();
  const appId = params.id;

  const switchOrganization = useCallback((orgId) => {
    const path = `/apps/${appId}`;
    const sub_path = window?.public_config?.SUB_PATH ? stripTrailingSlash(window?.public_config?.SUB_PATH) : '';
    organizationService.switchOrganization(orgId).then(
      () => {
        window.location.href = `${sub_path}/${orgId}${path}`;
      },
      () => {
        return (window.location.href = `${sub_path}/login/${orgId}?redirectTo=${path}`);
      }
    );
  }, [appId]);

  useEffect(() => loadAppDetails(appId), [appId]);

  return config.ENABLE_MULTIPLAYER_EDITING ? <RealtimeEditor {...props} /> : <Editor {...props} />;
}
Brief description and explanation of the suggested improvement.
The suggested improvements aim to optimize the performance of the component by reducing unnecessary function redefinitions and ensuring that the loadAppDetails function is called whenever appId changes. The useCallback hook is used to memoize the switchOrganization function, which prevents a new function from being created on every render. The loadAppDetails and handleError functions are moved outside of the component to prevent them from being redefined on every render. Finally, appId is added to the dependency array of the useEffect hook to ensure that the loadAppDetails function is called whenever appId changes.
```


## Example 2:

### Code Snippet:
```
render() {
    const { updateAvailable, darkMode } = this.state;
    let toastOptions = {
      style: {
        wordBreak: 'break-all',
      },
    };

    if (darkMode) {
      toastOptions = {
        className: 'toast-dark-mode',
        style: {
          borderRadius: '10px',
          background: '#333',
          color: '#fff',
          wordBreak: 'break-all',
        },
      };
    }
    const { sidebarNav } = this.state;
    const { updateSidebarNAV } = this;
    return (
      <>
        <div className={`main-wrapper ${darkMode ? 'theme-dark dark-theme' : ''}`} data-cy="main-wrapper">
          {updateAvailable && (
            <div className="alert alert-info alert-dismissible" role="alert">
              <h3 className="mb-1">Update available</h3>
              <p>A new version of ToolJet has been released.</p>
              <div className="btn-list">
                <a
                  href="https://docs.tooljet.io/docs/setup/updating"
                  target="_blank"
                  className="btn btn-info"
                  rel="noreferrer"
                >
                  Read release notes & update
                </a>
                <a
                  onClick={() => {
                    tooljetService.skipVersion();
                    this.setState({ updateAvailable: false });
                  }}
                  className="btn"
                >
                  Skip this version
                </a>
              </div>
            </div>
          )}
          <BreadCrumbContext.Provider value={{ sidebarNav, updateSidebarNAV }}>
            <Routes>
              <Route path="/login/:organizationId" exact element={<LoginPage />} />
              <Route path="/login" exact element={<LoginPage />} />
              <Route path="/setup" exact element={<SetupScreenSelfHost {...this.props} darkMode={darkMode} />} />
              <Route path="/sso/:origin/:configId" exact element={<Oauth />} />
              <Route path="/sso/:origin" exact element={<Oauth />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/reset-password/:token" element={<ResetPassword />} />
              <Route path="/reset-password" element={<ResetPassword />} />
              <Route path="/invitations/:token" element={<VerificationSuccessInfoScreen />} />
              <Route
                path="/invitations/:token/workspaces/:organizationToken"
                element={<VerificationSuccessInfoScreen />}
              />
              <Route path="/confirm" element={<VerificationSuccessInfoScreen />} />
              <Route
                path="/organization-invitations/:token"
                element={<OrganizationInvitationPage {...this.props} darkMode={darkMode} />}
              />
              <Route
                path="/confirm-invite"
                element={<OrganizationInvitationPage {...this.props} darkMode={darkMode} />}
              />
              <Route
                exact
                path="/:workspaceId/apps/:id/:pageHandle?/*"
                element={
                  <PrivateRoute>
                    <AppLoader switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              <Route
                exact
                path="/applications/:id/versions/:versionId/:pageHandle?"
                element={
                  <PrivateRoute>
                    <Viewer switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              <Route
                exact
                path="/applications/:slug/:pageHandle?"
                element={
                  <PrivateRoute>
                    <Viewer switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              <Route
                exact
                path="/oauth2/authorize"
                element={
                  <PrivateRoute>
                    <Authorize switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              <Route
                exact
                path="/:workspaceId/workspace-settings"
                element={
                  <PrivateRoute>
                    <OrganizationSettings switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              <Route
                exact
                path="/:workspaceId/settings"
                element={
                  <PrivateRoute>
                    <SettingsPage switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              <Route
                exact
                path="/:workspaceId/data-sources"
                element={
                  <PrivateRoute>
                    <GlobalDatasources switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              {window.public_config?.ENABLE_TOOLJET_DB == 'true' && (
                <Route
                  exact
                  path="/:workspaceId/database"
                  element={
                    <PrivateRoute>
                      <TooljetDatabase switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                    </PrivateRoute>
                  }
                />
              )}

              {window.public_config?.ENABLE_MARKETPLACE_FEATURE === 'true' && (
                <Route
                  exact
                  path="/integrations"
                  element={
                    <AdminRoute>
                      <MarketplacePage switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                    </AdminRoute>
                  }
                />
              )}
              <Route exact path="/" element={<Navigate to="/:workspaceId" />} />
              <Route
                exact
                path="/switch-workspace"
                element={
                  <PrivateRoute>
                    <SwitchWorkspacePage switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              <Route
                exact
                path="/:workspaceId"
                element={
                  <PrivateRoute>
                    <HomePage switchDarkMode={this.switchDarkMode} darkMode={darkMode} />
                  </PrivateRoute>
                }
              />
              <Route
                path="*"
                render={() => {
                  if (authenticationService?.currentSessionValue?.current_organization_id) {
                    return <Navigate to="/:workspaceId" />;
                  }
                  return <Navigate to="/login" />;
                }}
              />
            </Routes>
          </BreadCrumbContext.Provider>
        </div>

        <Toast toastOptions={toastOptions} />
      </>
    );
  }
}
```
### Result
```
Current Performance Limitation
The current code is reassigning the toastOptions object every time the render function is called and the darkMode state is true. This could potentially slow down the rendering process as it involves creating a new object and garbage collection of the old one.

Improvement Steps
Instead of reassigning the toastOptions object, we can directly assign the properties to the existing object when darkMode is true. This avoids creating a new object and the associated garbage collection.
Improved Code
render() {
    const { updateAvailable, darkMode } = this.state;
    let toastOptions = {
      style: {
        wordBreak: 'break-all',
      },
    };

    if (darkMode) {
      toastOptions.className = 'toast-dark-mode';
      toastOptions.style = {
        ...toastOptions.style,
        borderRadius: '10px',
        background: '#333',
        color: '#fff',
      };
    }
    // Rest of the code remains the same...
}
Explanation of the Improvement
The improved code directly assigns the properties to the toastOptions object when darkMode is true, instead of creating a new object. This reduces the overhead of object creation and garbage collection, potentially improving the performance of the render function.
```

## Example 3:

### Code Snippet:
```
class CartModel extends Model {
    constructor(cart, linked) {
        super();
        this.cart = cart;
        this.items = cart.items;
        this._filteredItems = [...this.items];
        this.linked = linked;
    }

    get filteredItems() {
        return this._filteredItems;
    }

    set filteredItems(newItems) {
        this._filteredItems = newItems;
        this.notify();
    }
}
```
### Result
```
No clear performance improvements found.
```

## Example 3:

### Code Snippet:
```
// Process redirects before running anything else
if (location.href.includes("heissepreise.github.io")) {
    location.href = "https://heisse-preise.io";
    return;
}

const { getQueryParameter } = require("./js/misc");
const model = require("./model");
require("./views");

const { STORE_KEYS } = require("./model/stores");
const { ProgressBar } = require("./views/progress-bar");
const progressBar = new ProgressBar(STORE_KEYS.length);

(async () => {
    await model.load(() => progressBar.addStep());
    const itemsFilter = document.querySelector("items-filter");
    const itemsList = document.querySelector("items-list");
    const itemsChart = document.querySelector("items-chart");

    const stateToUrl = (event) => {
        const filterState = itemsFilter.shareableState;
        const listState = itemsList.shareableState;
        const chartState = itemsChart.shareableState;
        const chartedItems = model.items.filteredItems
            .filter((item) => item.chart)
            .map((item) => item.store + item.id)
            .join(";");

        history.replaceState({}, null, location.pathname + "?f=" + filterState + "&l=" + listState + "&c=" + chartState + "&d=" + chartedItems);
    };

    itemsFilter.addEventListener("x-change", stateToUrl);
    itemsList.addEventListener("x-change", stateToUrl);

    const f = getQueryParameter("f");
    const l = getQueryParameter("l");
    const c = getQueryParameter("c");
    const d = getQueryParameter("d");
    if (f) itemsFilter.shareableState = f;
    if (l) itemsList.shareableState = l;
    if (c) itemsChart.shareableState = c;
    if (d) {
        for (const id of d.split(";")) {
            model.items.lookup[id].chart = true;
        }
    }
    itemsFilter.model = itemsList.model = model.items;
    itemsFilter.fireChangeEvent();
})();
```
### Result
```
Current Performance Limitation
The current code is not optimized for performance due to the following reasons:

The code is using querySelector multiple times to select the same elements. This is inefficient as querySelector is a relatively expensive operation.
The stateToUrl function is called multiple times for each change event. This could lead to unnecessary computations and updates to the browser's history state.
The code is using split and a loop to update the chart property of each item in the model. This could be optimized using a more efficient data structure.
Improvement Steps
Store the selected elements in variables to avoid calling querySelector multiple times.
Debounce the stateToUrl function to limit the number of times it is called.
Use a Set to store the ids of items that should have their chart property set to true. This will make the lookup operation more efficient.
Improved Code
// Process redirects before running anything else
if (location.href.includes("heissepreise.github.io")) {
    location.href = "https://heisse-preise.io";
    return;
}

const { getQueryParameter, debounce } = require("./js/misc");
const model = require("./model");
require("./views");

const { STORE_KEYS } = require("./model/stores");
const { ProgressBar } = require("./views/progress-bar");
const progressBar = new ProgressBar(STORE_KEYS.length);

const itemsFilter = document.querySelector("items-filter");
const itemsList = document.querySelector("items-list");
const itemsChart = document.querySelector("items-chart");

const stateToUrl = debounce((event) => {
    const filterState = itemsFilter.shareableState;
    const listState = itemsList.shareableState;
    const chartState = itemsChart.shareableState;
    const chartedItems = model.items.filteredItems
        .filter((item) => item.chart)
        .map((item) => item.store + item.id)
        .join(";");

    history.replaceState({}, null, location.pathname + "?f=" + filterState + "&l=" + listState + "&c=" + chartState + "&d=" + chartedItems);
}, 250);

itemsFilter.addEventListener("x-change", stateToUrl);
itemsList.addEventListener("x-change", stateToUrl);

(async () => {
    await model.load(() => progressBar.addStep());

    const f = getQueryParameter("f");
    const l = getQueryParameter("l");
    const c = getQueryParameter("c");
    const d = getQueryParameter("d");
    if (f) itemsFilter.shareableState = f;
    if (l) itemsList.shareableState = l;
    if (c) itemsChart.shareableState = c;
    if (d) {
        const chartedIds = new Set(d.split(";"));
        for (const item of model.items.lookup) {
            if (chartedIds.has(item.store + item.id)) {
                item.chart = true;
            }
        }
    }
    itemsFilter.model = itemsList.model = model.items;
    itemsFilter.fireChangeEvent();
})();
Explanation of the Improvement
By storing the selected elements in variables, we avoid the need to call querySelector multiple times, which improves performance.
The debounce function limits the number of times stateToUrl is called, reducing unnecessary computations and updates to the browser's history state.
Using a Set for chartedIds makes the lookup operation more efficient, which can significantly improve performance when dealing with large data sets.
```

# Java Examples

## Example 1:

### Code Snippet:
```
	 public static void main(String[] args) throws IOException {
		 System.out.println("Heap space available is " + Runtime.getRuntime().maxMemory());
 
		 var mGrid = List.of(8, 12, 16, 24, 32, 48, 64);
		 var efConstructionGrid = List.of(60, 80, 100, 120, 160, 200, 400, 600, 800);
		 var efSearchGrid = List.of(1, 2);
		 var diskGrid = List.of(false, true);
 
		 // this dataset contains more than 10k query vectors, so we limit it with .subList
		 var adaSet = loadWikipediaData();
		 gridSearch(adaSet, mGrid, efConstructionGrid, diskGrid, efSearchGrid);
 
		 var files = List.of(
				 // large files not yet supported
				 // "hdf5/deep-image-96-angular.hdf5",
				 // "hdf5/gist-960-euclidean.hdf5",
				 "hdf5/nytimes-256-angular.hdf5",
				 "hdf5/glove-100-angular.hdf5",
				 "hdf5/glove-200-angular.hdf5",
				 "hdf5/sift-128-euclidean.hdf5");
		 for (var f : files) {
			 gridSearch(Hdf5Loader.load(f), mGrid, efConstructionGrid, diskGrid, efSearchGrid);
		 }
 
		 // tiny dataset, don't waste time building a huge index
		 files = List.of("hdf5/fashion-mnist-784-euclidean.hdf5");
		 mGrid = List.of(8, 12, 16, 24);
		 efConstructionGrid = List.of(40, 60, 80, 100, 120, 160);
		 for (var f : files) {
			 gridSearch(Hdf5Loader.load(f), mGrid, efConstructionGrid, diskGrid, efSearchGrid);
		 }
	 }
```
### Result
```
No clear performance improvements found.
```

## Example 2:

### Code Snippet:
```
final class SimdOps {

    static final boolean HAS_AVX512 = IntVector.SPECIES_PREFERRED == IntVector.SPECIES_512;
    static final IntVector BYTE_TO_INT_MASK_512 = IntVector.broadcast(IntVector.SPECIES_512, 0xff);
    static final IntVector BYTE_TO_INT_MASK_256 = IntVector.broadcast(IntVector.SPECIES_256, 0xff);

    static final ThreadLocal<int[]> scratchInt512 = ThreadLocal.withInitial(() -> new int[IntVector.SPECIES_512.length()]);
    static final ThreadLocal<int[]> scratchInt256 = ThreadLocal.withInitial(() -> new int[IntVector.SPECIES_256.length()]);


    static float sum(float[] vector) {
        var sum = FloatVector.zero(FloatVector.SPECIES_PREFERRED);
        int vectorizedLength = FloatVector.SPECIES_PREFERRED.loopBound(vector.length);

        // Process the vectorized part
        for (int i = 0; i < vectorizedLength; i += FloatVector.SPECIES_PREFERRED.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, vector, i);
            sum = sum.add(a);
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (int i = vectorizedLength; i < vector.length; i++) {
            res += vector[i];
        }

        return res;
    }

    static float[] sum(List<float[]> vectors) {
        if (vectors == null || vectors.isEmpty()) {
            throw new IllegalArgumentException("Input list cannot be null or empty");
        }

        int dimension = vectors.get(0).length;
        float[] sum = new float[dimension];

        // Process each vector from the list
        for (float[] vector : vectors) {
            addInPlace(sum, vector);
        }

        return sum;
    }

    static void divInPlace(float[] vector, float divisor) {
        int vectorizedLength = FloatVector.SPECIES_PREFERRED.loopBound(vector.length);

        // Process the vectorized part
        for (int i = 0; i < vectorizedLength; i += FloatVector.SPECIES_PREFERRED.length()) {
            var a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, vector, i);
            var divResult = a.div(divisor);
            divResult.intoArray(vector, i);
        }

        // Process the tail
        for (int i = vectorizedLength; i < vector.length; i++) {
            vector[i] = vector[i] / divisor;
        }
    }

    static float dot64(float[] v1, int offset1, float[] v2, int offset2) {
        var a = FloatVector.fromArray(FloatVector.SPECIES_64, v1, offset1);
        var b = FloatVector.fromArray(FloatVector.SPECIES_64, v2, offset2);
        return a.mul(b).reduceLanes(VectorOperators.ADD);
    }

    static float dot128(float[] v1, int offset1, float[] v2, int offset2) {
        var a = FloatVector.fromArray(FloatVector.SPECIES_128, v1, offset1);
        var b = FloatVector.fromArray(FloatVector.SPECIES_128, v2, offset2);
        return a.mul(b).reduceLanes(VectorOperators.ADD);
    }

    static float dot256(float[] v1, int offset1, float[] v2, int offset2) {
        var a = FloatVector.fromArray(FloatVector.SPECIES_256, v1, offset1);
        var b = FloatVector.fromArray(FloatVector.SPECIES_256, v2, offset2);
        return a.mul(b).reduceLanes(VectorOperators.ADD);
    }

    static float dotPreferred(float[] v1, int offset1, float[] v2, int offset2) {
        var a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v1, offset1);
        var b = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v2, offset2);
        return a.mul(b).reduceLanes(VectorOperators.ADD);
    }

    static float dotProduct(float[] v1, float[] v2) {
        return dotProduct(v1, 0, v2, 0, v1.length);
    }

    static float dotProduct(float[] v1, int v1offset, float[] v2, int v2offset, final int length)
    {
        //Common case first
        if (length >= FloatVector.SPECIES_PREFERRED.length())
            return dotProductPreferred(v1, v1offset, v2, v2offset, length);

        if (length < FloatVector.SPECIES_128.length())
            return dotProduct64(v1, v1offset, v2, v2offset, length);
        else if (length < FloatVector.SPECIES_256.length())
            return dotProduct128(v1, v1offset, v2, v2offset, length);
        else
            return dotProduct256(v1, v1offset, v2, v2offset, length);

    }

    static float dotProduct64(float[] v1, int v1offset, float[] v2, int v2offset, int length) {

        if (length == FloatVector.SPECIES_64.length())
            return dot64(v1, v1offset, v2, v2offset);

        final int vectorizedLength = FloatVector.SPECIES_64.loopBound(length);
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_64);

        int i = 0;
        // Process the vectorized part
        for (; i < vectorizedLength; i += FloatVector.SPECIES_64.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_64, v1, v1offset + i);
            FloatVector b = FloatVector.fromArray(FloatVector.SPECIES_64, v2, v2offset + i);
            sum = sum.add(a.mul(b));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (; i < length; ++i)
            res += v1[v1offset + i] * v2[v2offset + i];

        return res;
    }

    static float dotProduct128(float[] v1, int v1offset, float[] v2, int v2offset, int length) {

        if (length == FloatVector.SPECIES_128.length())
            return dot128(v1, v1offset, v2, v2offset);

        final int vectorizedLength = FloatVector.SPECIES_128.loopBound(length);
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_128);

        int i = 0;
        // Process the vectorized part
        for (; i < vectorizedLength; i += FloatVector.SPECIES_128.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_128, v1, v1offset + i);
            FloatVector b = FloatVector.fromArray(FloatVector.SPECIES_128, v2, v2offset + i);
            sum = sum.add(a.mul(b));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (; i < length; ++i)
            res += v1[v1offset + i] * v2[v2offset + i];

        return res;
    }


    static float dotProduct256(float[] v1, int v1offset, float[] v2, int v2offset, int length) {

        if (length == FloatVector.SPECIES_256.length())
            return dot256(v1, v1offset, v2, v2offset);

        final int vectorizedLength = FloatVector.SPECIES_256.loopBound(length);
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_256);

        int i = 0;
        // Process the vectorized part
        for (; i < vectorizedLength; i += FloatVector.SPECIES_256.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_256, v1, v1offset + i);
            FloatVector b = FloatVector.fromArray(FloatVector.SPECIES_256, v2, v2offset + i);
            sum = sum.add(a.mul(b));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (; i < length; ++i)
            res += v1[v1offset + i] * v2[v2offset + i];

        return res;
    }

    static float dotProductPreferred(float[] v1, int v1offset, float[] v2, int v2offset, int length) {

        if (length == FloatVector.SPECIES_PREFERRED.length())
            return dotPreferred(v1, v1offset, v2, v2offset);

        final int vectorizedLength = FloatVector.SPECIES_PREFERRED.loopBound(length);
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_PREFERRED);

        int i = 0;
        // Process the vectorized part
        for (; i < vectorizedLength; i += FloatVector.SPECIES_PREFERRED.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v1, v1offset + i);
            FloatVector b = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v2, v2offset + i);
            sum = sum.add(a.mul(b));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (; i < length; ++i)
            res += v1[v1offset + i] * v2[v2offset + i];

        return res;
    }

    static int dotProduct(byte[] v1, byte[] v2) {
        if (v1.length != v2.length) {
            throw new IllegalArgumentException("Vectors must have the same length");
        }
        var sum = IntVector.zero(IntVector.SPECIES_256);
        int vectorizedLength = ByteVector.SPECIES_64.loopBound(v1.length);

        // Process the vectorized part, convert from 8 bytes to 8 ints
        for (int i = 0; i < vectorizedLength; i += ByteVector.SPECIES_64.length()) {
            var a = ByteVector.fromArray(ByteVector.SPECIES_64, v1, i).castShape(IntVector.SPECIES_256, 0);
            var b = ByteVector.fromArray(ByteVector.SPECIES_64, v2, i).castShape(IntVector.SPECIES_256, 0);
            sum = sum.add(a.mul(b));
        }

        int res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (int i = vectorizedLength; i < v1.length; i++) {
            res += v1[i] * v2[i];
        }

        return res;
    }

    static float cosineSimilarity(float[] v1, float[] v2) {
        if (v1.length != v2.length) {
            throw new IllegalArgumentException("Vectors must have the same length");
        }

        var vsum = FloatVector.zero(FloatVector.SPECIES_PREFERRED);
        var vaMagnitude = FloatVector.zero(FloatVector.SPECIES_PREFERRED);
        var vbMagnitude = FloatVector.zero(FloatVector.SPECIES_PREFERRED);

        int vectorizedLength = FloatVector.SPECIES_PREFERRED.loopBound(v1.length);
        // Process the vectorized part, convert from 8 bytes to 8 ints
        for (int i = 0; i < vectorizedLength; i += FloatVector.SPECIES_PREFERRED.length()) {
            var a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v1, i);
            var b = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v2, i);
            vsum = vsum.add(a.mul(b));
            vaMagnitude = vaMagnitude.add(a.mul(a));
            vbMagnitude = vbMagnitude.add(b.mul(b));
        }

        float sum = vsum.reduceLanes(VectorOperators.ADD);
        float aMagnitude = vaMagnitude.reduceLanes(VectorOperators.ADD);
        float bMagnitude = vbMagnitude.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (int i = vectorizedLength; i < v1.length; i++) {
            sum += v1[i] * v2[i];
            aMagnitude += v1[i] * v1[i];
            bMagnitude += v2[i] * v2[i];
        }

        return (float) (sum / Math.sqrt(aMagnitude * bMagnitude));
    }

    static float cosineSimilarity(byte[] v1, byte[] v2) {
        if (v1.length != v2.length) {
            throw new IllegalArgumentException("Vectors must have the same length");
        }

        var vsum = IntVector.zero(IntVector.SPECIES_256);
        var vaMagnitude = IntVector.zero(IntVector.SPECIES_256);
        var vbMagnitude = IntVector.zero(IntVector.SPECIES_256);

        int vectorizedLength = ByteVector.SPECIES_64.loopBound(v1.length);
        // Process the vectorized part, convert from 8 bytes to 8 ints
        for (int i = 0; i < vectorizedLength; i += ByteVector.SPECIES_64.length()) {
            var a = ByteVector.fromArray(ByteVector.SPECIES_64, v1, i).castShape(IntVector.SPECIES_256, 0);
            var b = ByteVector.fromArray(ByteVector.SPECIES_64, v2, i).castShape(IntVector.SPECIES_256, 0);
            vsum = vsum.add(a.mul(b));
            vaMagnitude = vaMagnitude.add(a.mul(a));
            vbMagnitude = vbMagnitude.add(b.mul(b));
        }

        int sum = vsum.reduceLanes(VectorOperators.ADD);
        int aMagnitude = vaMagnitude.reduceLanes(VectorOperators.ADD);
        int bMagnitude = vbMagnitude.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (int i = vectorizedLength; i < v1.length; i++) {
            sum += v1[i] * v2[i];
            aMagnitude += v1[i] * v1[i];
            bMagnitude += v2[i] * v2[i];
        }

        return (float) (sum / Math.sqrt(aMagnitude * bMagnitude));
    }

    static float squareDistance64(float[] v1, int offset1, float[] v2, int offset2) {
        var a = FloatVector.fromArray(FloatVector.SPECIES_64, v1, offset1);
        var b = FloatVector.fromArray(FloatVector.SPECIES_64, v2, offset2);
        var diff = a.sub(b);
        return diff.mul(diff).reduceLanes(VectorOperators.ADD);
    }

    static float squareDistance128(float[] v1, int offset1, float[] v2, int offset2) {
        var a = FloatVector.fromArray(FloatVector.SPECIES_128, v1, offset1);
        var b = FloatVector.fromArray(FloatVector.SPECIES_128, v2, offset2);
        var diff = a.sub(b);
        return diff.mul(diff).reduceLanes(VectorOperators.ADD);
    }

    static float squareDistance256(float[] v1, int offset1, float[] v2, int offset2) {
        var a = FloatVector.fromArray(FloatVector.SPECIES_256, v1, offset1);
        var b = FloatVector.fromArray(FloatVector.SPECIES_256, v2, offset2);
        var diff = a.sub(b);
        return diff.mul(diff).reduceLanes(VectorOperators.ADD);
    }

    static float squareDistancePreferred(float[] v1, int offset1, float[] v2, int offset2) {
        var a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v1, offset1);
        var b = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v2, offset2);
        var diff = a.sub(b);
        return diff.mul(diff).reduceLanes(VectorOperators.ADD);
    }

    static float squareDistance(float[] v1, float[] v2) {
        return squareDistance(v1, 0, v2, 0, v1.length);
    }

    static float squareDistance(float[] v1, int v1offset, float[] v2, int v2offset, final int length)
    {
        //Common case first
        if (length >= FloatVector.SPECIES_PREFERRED.length())
            return squareDistancePreferred(v1, v1offset, v2, v2offset, length);

        if (length < FloatVector.SPECIES_128.length())
            return squareDistance64(v1, v1offset, v2, v2offset, length);
        else if (length < FloatVector.SPECIES_256.length())
            return squareDistance128(v1, v1offset, v2, v2offset, length);
        else
            return squareDistance256(v1, v1offset, v2, v2offset, length);
    }

    static float squareDistance64(float[] v1, int v1offset, float[] v2, int v2offset, int length) {
        if (length == FloatVector.SPECIES_64.length())
            return squareDistance64(v1, v1offset, v2, v2offset);

        final int vectorizedLength = FloatVector.SPECIES_64.loopBound(length);
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_64);

        int i = 0;
        // Process the vectorized part
        for (; i < vectorizedLength; i += FloatVector.SPECIES_64.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_64, v1, v1offset + i);
            FloatVector b = FloatVector.fromArray(FloatVector.SPECIES_64, v2, v2offset + i);
            var diff = a.sub(b);
            sum = sum.add(diff.mul(diff));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (; i < length; ++i) {
            var diff = v1[v1offset + i] - v2[v2offset + i];
            res += diff * diff;
        }

        return res;
    }

    static float squareDistance128(float[] v1, int v1offset, float[] v2, int v2offset, int length) {
        if (length == FloatVector.SPECIES_128.length())
            return squareDistance128(v1, v1offset, v2, v2offset);

        final int vectorizedLength = FloatVector.SPECIES_128.loopBound(length);
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_128);

        int i = 0;
        // Process the vectorized part
        for (; i < vectorizedLength; i += FloatVector.SPECIES_128.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_128, v1, v1offset + i);
            FloatVector b = FloatVector.fromArray(FloatVector.SPECIES_128, v2, v2offset + i);
            var diff = a.sub(b);
            sum = sum.add(diff.mul(diff));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (; i < length; ++i) {
            var diff = v1[v1offset + i] - v2[v2offset + i];
            res += diff * diff;
        }

        return res;
    }


    static float squareDistance256(float[] v1, int v1offset, float[] v2, int v2offset, int length) {
        if (length == FloatVector.SPECIES_256.length())
            return squareDistance256(v1, v1offset, v2, v2offset);

        final int vectorizedLength = FloatVector.SPECIES_256.loopBound(length);
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_256);

        int i = 0;
        // Process the vectorized part
        for (; i < vectorizedLength; i += FloatVector.SPECIES_256.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_256, v1, v1offset + i);
            FloatVector b = FloatVector.fromArray(FloatVector.SPECIES_256, v2, v2offset + i);
            var diff = a.sub(b);
            sum = sum.add(diff.mul(diff));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (; i < length; ++i) {
            var diff = v1[v1offset + i] - v2[v2offset + i];
            res += diff * diff;
        }

        return res;
    }

    static float squareDistancePreferred(float[] v1, int v1offset, float[] v2, int v2offset, int length) {

        if (length == FloatVector.SPECIES_PREFERRED.length())
            return squareDistancePreferred(v1, v1offset, v2, v2offset);

        final int vectorizedLength = FloatVector.SPECIES_PREFERRED.loopBound(length);
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_PREFERRED);

        int i = 0;
        // Process the vectorized part
        for (; i < vectorizedLength; i += FloatVector.SPECIES_PREFERRED.length()) {
            FloatVector a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v1, v1offset + i);
            FloatVector b = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v2, v2offset + i);
            var diff = a.sub(b);
            sum = sum.add(diff.mul(diff));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (; i < length; ++i) {
            var diff = v1[v1offset + i] - v2[v2offset + i];
            res += diff * diff;
        }

        return res;
    }

    static int squareDistance(byte[] v1, byte[] v2) {
        if (v1.length != v2.length) {
            throw new IllegalArgumentException("Vectors must have the same length");
        }

        var vdiffSumSquared = IntVector.zero(IntVector.SPECIES_256);

        int vectorizedLength = ByteVector.SPECIES_64.loopBound(v1.length);
        // Process the vectorized part
        for (int i = 0; i < vectorizedLength; i += ByteVector.SPECIES_64.length()) {
            var a = ByteVector.fromArray(ByteVector.SPECIES_64, v1, i).castShape(IntVector.SPECIES_256, 0);
            var b = ByteVector.fromArray(ByteVector.SPECIES_64, v2, i).castShape(IntVector.SPECIES_256, 0);

            var diff = a.sub(b);
            vdiffSumSquared = vdiffSumSquared.add(diff.mul(diff));
        }

        int diffSumSquared = vdiffSumSquared.reduceLanes(VectorOperators.ADD);

        // Process the tail
        for (int i = vectorizedLength; i < v1.length; i++) {
            diffSumSquared += (v1[i] - v2[i]) * (v1[i] - v2[i]);
        }

        return diffSumSquared;
    }

    static void addInPlace(float[] v1, float[] v2) {
        if (v1.length != v2.length) {
            throw new IllegalArgumentException("Vectors must have the same length");
        }

        int vectorizedLength = FloatVector.SPECIES_PREFERRED.loopBound(v1.length);

        // Process the vectorized part
        for (int i = 0; i < vectorizedLength; i += FloatVector.SPECIES_PREFERRED.length()) {
            var a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v1, i);
            var b = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v2, i);
            a.add(b).intoArray(v1, i);
        }

        // Process the tail
        for (int i = vectorizedLength; i < v1.length; i++) {
            v1[i] = v1[i] + v2[i];
        }
    }

    static void subInPlace(float[] v1, float[] v2) {
        if (v1.length != v2.length) {
            throw new IllegalArgumentException("Vectors must have the same length");
        }

        int vectorizedLength = FloatVector.SPECIES_PREFERRED.loopBound(v1.length);

        // Process the vectorized part
        for (int i = 0; i < vectorizedLength; i += FloatVector.SPECIES_PREFERRED.length()) {
            var a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v1, i);
            var b = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, v2, i);
            a.sub(b).intoArray(v1, i);
        }

        // Process the tail
        for (int i = vectorizedLength; i < v1.length; i++) {
            v1[i] = v1[i] - v2[i];
        }
    }

    static float[] sub(float[] lhs, float[] rhs) {
        if (lhs.length != rhs.length) {
            throw new IllegalArgumentException("Vectors must have the same length");
        }

        float[] result = new float[lhs.length];
        int vectorizedLength = (lhs.length / FloatVector.SPECIES_PREFERRED.length()) * FloatVector.SPECIES_PREFERRED.length();

        // Process the vectorized part
        for (int i = 0; i < vectorizedLength; i += FloatVector.SPECIES_PREFERRED.length()) {
            var a = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, lhs, i);
            var b = FloatVector.fromArray(FloatVector.SPECIES_PREFERRED, rhs, i);
            var subResult = a.sub(b);
            subResult.intoArray(result, i);
        }

        // Process the tail
        for (int i = vectorizedLength; i < lhs.length; i++) {
            result[i] = lhs[i] - rhs[i];
        }

        return result;
    }

    static float assembleAndSum(float[] data, int dataBase, byte[] baseOffsets) {
        return HAS_AVX512 ? assembleAndSum512(data, dataBase, baseOffsets)
               : assembleAndSum256(data, dataBase, baseOffsets);
    }

    static float assembleAndSum512(float[] data, int dataBase, byte[] baseOffsets) {
        int[] convOffsets = scratchInt512.get();
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_512);
        int i = 0;
        int limit = ByteVector.SPECIES_128.loopBound(baseOffsets.length);

        for (; i < limit; i += ByteVector.SPECIES_128.length()) {
            var scale = IntVector.zero(IntVector.SPECIES_512).addIndex(1).add(i).mul(dataBase);

            ByteVector.fromArray(ByteVector.SPECIES_128, baseOffsets, i)
                    .convertShape(VectorOperators.B2I, IntVector.SPECIES_512, 0)
                    .lanewise(VectorOperators.AND, BYTE_TO_INT_MASK_512)
                    .reinterpretAsInts()
                    .add(scale)
                    .intoArray(convOffsets,0);

            sum = sum.add(FloatVector.fromArray(FloatVector.SPECIES_512, data, 0, convOffsets, 0));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        //Process tail
        for (; i < baseOffsets.length; i++)
            res += data[dataBase * i + Byte.toUnsignedInt(baseOffsets[i])];

        return res;
    }

    static float assembleAndSum256(float[] data, int dataBase, byte[] baseOffsets) {
        int[] convOffsets = scratchInt256.get();
        FloatVector sum = FloatVector.zero(FloatVector.SPECIES_256);
        int i = 0;
        int limit = ByteVector.SPECIES_64.loopBound(baseOffsets.length);

        for (; i < limit; i += ByteVector.SPECIES_64.length()) {
            var scale = IntVector.zero(IntVector.SPECIES_256).addIndex(1).add(i).mul(dataBase);

            ByteVector.fromArray(ByteVector.SPECIES_64, baseOffsets, i)
                    .convertShape(VectorOperators.B2I, IntVector.SPECIES_256, 0)
                    .lanewise(VectorOperators.AND, BYTE_TO_INT_MASK_256)
                    .reinterpretAsInts()
                    .add(scale)
                    .intoArray(convOffsets,0);

            sum = sum.add(FloatVector.fromArray(FloatVector.SPECIES_256, data, 0, convOffsets, 0));
        }

        float res = sum.reduceLanes(VectorOperators.ADD);

        // Process tail
        for (; i < baseOffsets.length; i++)
            res += data[dataBase * i + Byte.toUnsignedInt(baseOffsets[i])];

        return res;
    }
}
```
### Result
```
No clear performance improvements found.
```

## Example 3:

### Code Snippet:
```
    public static void main(final String... args) {
        final String lsHome = System.getenv("LS_HOME");
        if (lsHome == null) {
            throw new IllegalStateException(
                    "LS_HOME environment variable must be set. This is likely a bug that should be reported."
            );
        }
        installGlobalUncaughtExceptionHandler();

        final Path home = Paths.get(lsHome).toAbsolutePath();
        try (
                final Logstash logstash = new Logstash(home, args, System.out, System.err, System.in)
        ) {
            logstash.run();
        } catch (final IllegalStateException e) {
            Throwable t = e;
            String message = e.getMessage();
            if (message != null) {
                if (message.startsWith(UNCLEAN_SHUTDOWN_PREFIX) ||
                    message.startsWith(MUTATED_GEMFILE_ERROR)) {
                    t = e.getCause(); // be less verbose with uncleanShutdown's wrapping exception
                } else if (message.contains("Could not load FFI Provider")) {
                    message =
                            "Error accessing temp directory: " + System.getProperty("java.io.tmpdir") +
                                    " this often occurs because the temp directory has been mounted with NOEXEC or" +
                                    " the Logstash user has insufficient permissions on the directory. \n" +
                                    "Possible workarounds include setting the -Djava.io.tmpdir property in the jvm.options" +
                                    "file to an alternate directory or correcting the Logstash user's permissions.";
                }
            }
            handleFatalError(message, t);
        } catch (final Throwable t) {
            handleFatalError("", t);
        }

        System.exit(0);
    }
```
### Result
```
No clear performance improvements found.
```

# Rust Examples

## Example 1:

### Code Snippet:
```
impl Cmd {
    #[tokio::main(flavor = "current_thread")]
    pub async fn run(self) -> Result<()> {
        Builder::new()
            .filter_level(log::LevelFilter::Off)
            .parse_env("ATUIN_LOG")
            .init();

        let mut settings = Settings::new().wrap_err("could not load client settings")?;

        let db_path = PathBuf::from(settings.db_path.as_str());
        let record_store_path = PathBuf::from(settings.record_store_path.as_str());

        let mut db = Sqlite::new(db_path).await?;
        let mut store = SqliteStore::new(record_store_path).await?;

        match self {
            Self::History(history) => history.run(&settings, &mut db).await,
            Self::Import(import) => import.run(&mut db).await,
            Self::Stats(stats) => stats.run(&mut db, &settings).await,
            Self::Search(search) => search.run(db, &mut settings).await,

            #[cfg(feature = "sync")]
            Self::Sync(sync) => sync.run(settings, &mut db, &mut store).await,

            #[cfg(feature = "sync")]
            Self::Account(account) => account.run(settings).await,

            Self::Kv(kv) => kv.run(&settings, &mut store).await,
        }
    }
}
```
### Result
```
No clear performance improvements found.
```

## Example 2:

### Code Snippet:
```
async fn compile(
    packages: Vec<&Package>,
    release_mode: bool,
    wasm: bool,
    project_path: PathBuf,
    target_path: impl Into<PathBuf>,
    deployment: bool,
    tx: Sender<Message>,
) -> anyhow::Result<Vec<BuiltService>> {
    let manifest_path = project_path.join("Cargo.toml");
    if !manifest_path.exists() {
        bail!("failed to read the Shuttle project manifest");
    }
    let target_path = target_path.into();

    let mut cargo = tokio::process::Command::new("cargo");
    cargo
        .arg("build")
        .arg("--manifest-path")
        .arg(manifest_path)
        .arg("--color=always") // piping disables auto color, but we want it
        .current_dir(project_path.as_path());

    if deployment {
        cargo.arg("--jobs=4");
    }

    for package in &packages {
        cargo.arg("--package").arg(package.name.as_str());
    }

    let profile = if release_mode {
        cargo.arg("--release");
        "release"
    } else {
        "debug"
    };

    if wasm {
        cargo.arg("--target").arg("wasm32-wasi");
    }

    let (reader, writer) = os_pipe::pipe()?;
    let writer_clone = writer.try_clone()?;
    cargo.stdout(writer);
    cargo.stderr(writer_clone);

    let mut handle = cargo.spawn()?;

    tokio::task::spawn_blocking(move || {
        let reader = std::io::BufReader::new(reader);
        for line in reader.lines() {
            if let Ok(line) = line {
                if let Err(error) = tx.send(Message::TextLine(line)) {
                    error!("failed to send cargo message on channel: {error}");
                };
            } else {
                error!("Failed to read Cargo log messages");
            };
        }
    });

    let command = handle.wait().await?;

    if !command.success() {
        bail!("Build failed. Is the Shuttle runtime missing?");
    }

    let services = packages
        .iter()
        .map(|package| {
            let path = if wasm {
                let mut path: PathBuf = [
                    project_path.clone(),
                    target_path.clone(),
                    "wasm32-wasi".into(),
                    profile.into(),
                    package.name.replace('-', "_").into(),
                ]
                .iter()
                .collect();
                path.set_extension("wasm");
                path
            } else {
                let mut path: PathBuf = [
                    project_path.clone(),
                    target_path.clone(),
                    profile.into(),
                    package.name.clone().into(),
                ]
                .iter()
                .collect();
                path.set_extension(std::env::consts::EXE_EXTENSION);
                path
            };

            BuiltService {
                workspace_path: project_path.clone(),
                manifest_path: package.manifest_path.clone().into_std_path_buf(),
                package_name: package.name.clone(),
                executable_path: path,
                is_wasm: wasm,
            }
        })
        .collect();

    Ok(services)
}
```
### Result
```
No clear performance improvements found.
```

## Example 3:

### Code Snippet:
```
use proc_macro::TokenStream;
use proc_macro2::Span;
use proc_macro_error::emit_error;
use quote::{quote, ToTokens};
use syn::{
    parse::Parse, parse_macro_input, parse_quote, punctuated::Punctuated, spanned::Spanned,
    Attribute, Expr, ExprLit, FnArg, Ident, ItemFn, Lit, Pat, PatIdent, Path, ReturnType,
    Signature, Stmt, Token, Type, TypePath,
};

pub(crate) fn r#impl(_attr: TokenStream, item: TokenStream) -> TokenStream {
    let mut fn_decl = parse_macro_input!(item as ItemFn);

    let loader = Loader::from_item_fn(&mut fn_decl);

    quote! {
        #[tokio::main]
        async fn main() {
            shuttle_runtime::start(loader).await;
        }

        #loader

        #fn_decl
    }
    .into()
}

struct Loader {
    fn_ident: Ident,
    fn_inputs: Vec<Input>,
    fn_return: TypePath,
}

#[derive(Debug, PartialEq)]
struct Input {
    /// The identifier for a resource input
    ident: Ident,

    /// The shuttle_runtime builder for this resource
    builder: Builder,
}

#[derive(Debug, PartialEq)]
struct Builder {
    /// Path to the builder
    path: Path,

    /// Options to call on the builder
    options: BuilderOptions,
}

#[derive(Debug, Default, PartialEq)]
struct BuilderOptions {
    /// The actual options
    options: Punctuated<BuilderOption, Token![,]>,
}

#[derive(Debug, PartialEq)]
struct BuilderOption {
    /// Identifier of the option to set
    ident: Ident,

    /// Value to set option to
    value: Expr,
}

impl Parse for BuilderOptions {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        Ok(Self {
            options: input.parse_terminated(BuilderOption::parse, Token![,])?,
        })
    }
}

impl Parse for BuilderOption {
    fn parse(input: syn::parse::ParseStream) -> syn::Result<Self> {
        let ident = input.parse()?;
        let _equal: Token![=] = input.parse()?;
        let value = input.parse()?;

        Ok(Self { ident, value })
    }
}

impl Loader {
    pub(crate) fn from_item_fn(item_fn: &mut ItemFn) -> Option<Self> {
        // rename function to allow any name, such as 'main'
        item_fn.sig.ident = Ident::new(
            &format!("__shuttle_{}", item_fn.sig.ident),
            Span::call_site(),
        );

        let inputs: Vec<_> = item_fn
            .sig
            .inputs
            .iter_mut()
            .filter_map(|input| match input {
                FnArg::Receiver(_) => None,
                FnArg::Typed(typed) => Some(typed),
            })
            .filter_map(|typed| match typed.pat.as_ref() {
                Pat::Ident(ident) => Some((ident, typed.attrs.drain(..).collect())),
                _ => None,
            })
            .filter_map(|(pat_ident, attrs)| {
                match attribute_to_builder(pat_ident, attrs) {
                    Ok(builder) => Some(Input {
                        ident: pat_ident.ident.clone(),
                        builder,
                    }),
                    Err(err) => {
                        emit_error!(pat_ident, err; hint = pat_ident.span() => "Try adding a config like `#[shuttle_shared_db::Postgres]`");
                        None
                    }
                }
            })
            .collect();

        check_return_type(item_fn.sig.clone()).map(|type_path| Self {
            fn_ident: item_fn.sig.ident.clone(),
            fn_inputs: inputs,
            fn_return: type_path,
        })
    }
}

fn check_return_type(signature: Signature) -> Option<TypePath> {
    match signature.output {
        ReturnType::Default => {
            emit_error!(
                signature,
                "shuttle_runtime::main functions need to return a service";
                hint = "See the docs for services with first class support";
                doc = "https://docs.rs/shuttle-service/latest/shuttle_service/attr.main.html#shuttle-supported-services"
            );
            None
        }
        ReturnType::Type(_, r#type) => match *r#type {
            Type::Path(path) => Some(path),
            _ => {
                emit_error!(
                    r#type,
                    "shuttle_runtime::main functions need to return a first class service or 'Result<impl Service, shuttle_runtime::Error>";
                    hint = "See the docs for services with first class support";
                    doc = "https://docs.rs/shuttle-service/latest/shuttle_service/attr.main.html#shuttle-supported-services"
                );
                None
            }
        },
    }
}

fn attribute_to_builder(pat_ident: &PatIdent, attrs: Vec<Attribute>) -> syn::Result<Builder> {
    if attrs.is_empty() {
        return Err(syn::Error::new_spanned(
            pat_ident,
            "resource needs an attribute configuration",
        ));
    }

    let options = if attrs[0].meta.require_list().is_err() {
        Default::default()
    } else {
        attrs[0].parse_args()?
    };

    let builder = Builder {
        path: attrs[0].path().clone(),
        options,
    };

    Ok(builder)
}

impl ToTokens for Loader {
    fn to_tokens(&self, tokens: &mut proc_macro2::TokenStream) {
        let fn_ident = &self.fn_ident;

        let return_type = &self.fn_return;

        let mut fn_inputs = Vec::with_capacity(self.fn_inputs.len());
        let mut fn_inputs_builder = Vec::with_capacity(self.fn_inputs.len());
        let mut fn_inputs_builder_options = Vec::with_capacity(self.fn_inputs.len());

        let mut needs_vars = false;

        for input in self.fn_inputs.iter() {
            fn_inputs.push(&input.ident);
            fn_inputs_builder.push(&input.builder.path);

            let (methods, values): (Vec<_>, Vec<_>) = input
                .builder
                .options
                .options
                .iter()
                .map(|o| {
                    let value = match &o.value {
                        Expr::Lit(ExprLit {
                            lit: Lit::Str(str), ..
                        }) => {
                            needs_vars = true;
                            quote!(&shuttle_runtime::strfmt(#str, &vars)?)
                        }
                        other => quote!(#other),
                    };

                    (&o.ident, value)
                })
                .unzip();
            let chain = quote!(#(.#methods(#values))*);
            fn_inputs_builder_options.push(chain);
        }

        let factory_ident: Ident = if self.fn_inputs.is_empty() {
            parse_quote!(_factory)
        } else {
            parse_quote!(factory)
        };

        let resource_tracker_ident: Ident = if self.fn_inputs.is_empty() {
            parse_quote!(_resource_tracker)
        } else {
            parse_quote!(resource_tracker)
        };

        let extra_imports: Option<Stmt> = if self.fn_inputs.is_empty() {
            None
        } else {
            Some(parse_quote!(
                use shuttle_runtime::{Factory, ResourceBuilder};
            ))
        };

        // variables for string interpolating secrets into the attribute macros
        let (vars, drop_vars): (Option<Stmt>, Option<Stmt>) = if needs_vars {
            (
                Some(parse_quote!(
                    let vars = std::collections::HashMap::from_iter(
                        factory
                            .get_secrets()
                            .await?
                            .into_iter()
                            .map(|(key, value)| (format!("secrets.{}", key), value))
                    );
                )),
                Some(parse_quote!(
                    std::mem::drop(vars);
                )),
            )
        } else {
            (None, None)
        };

        let loader = quote! {
            async fn loader(
                mut #factory_ident: shuttle_runtime::ProvisionerFactory,
                mut #resource_tracker_ident: shuttle_runtime::ResourceTracker,
            ) -> #return_type {
                use shuttle_runtime::Context;
                #extra_imports
                #vars
                #(let #fn_inputs = shuttle_runtime::get_resource(
                    #fn_inputs_builder::new()#fn_inputs_builder_options,
                    &mut #factory_ident,
                    &mut #resource_tracker_ident,
                )
                .await.context(format!("failed to provision {}", stringify!(#fn_inputs_builder)))?;)*

                #drop_vars

                #fn_ident(#(#fn_inputs),*).await
            }
        };

        loader.to_tokens(tokens);
    }
}

#[cfg(test)]
mod tests {
    use pretty_assertions::assert_eq;
    use quote::quote;
    use syn::{parse_quote, Ident, TypePath};

    use super::{Builder, BuilderOptions, Input, Loader};

    #[test]
    fn from_with_return() {
        let mut input = parse_quote!(
            async fn simple() -> ShuttleAxum {}
        );

        let actual = Loader::from_item_fn(&mut input).unwrap();
        let expected_ident: Ident = parse_quote!(__shuttle_simple);
        let expected_return: TypePath = parse_quote!(ShuttleAxum);

        assert_eq!(actual.fn_ident, expected_ident);
        assert_eq!(actual.fn_inputs, Vec::<Input>::new());
        assert_eq!(actual.fn_return, expected_return);
    }

    #[test]
    fn from_with_main() {
        let mut input = parse_quote!(
            async fn main() -> ShuttleAxum {}
        );

        let actual = Loader::from_item_fn(&mut input).unwrap();
        let expected_ident: Ident = parse_quote!(__shuttle_main);

        assert_eq!(actual.fn_ident, expected_ident);
    }

    #[test]
    fn output_with_return() {
        let input = Loader {
            fn_ident: parse_quote!(simple),
            fn_inputs: Vec::new(),
            fn_return: parse_quote!(ShuttleSimple),
        };

        let actual = quote!(#input);
        let expected = quote! {
            async fn loader(
                mut _factory: shuttle_runtime::ProvisionerFactory,
                mut _resource_tracker: shuttle_runtime::ResourceTracker,
            ) -> ShuttleSimple {
                use shuttle_runtime::Context;
                simple().await
            }
        };

        assert_eq!(actual.to_string(), expected.to_string());
    }

    #[test]
    fn from_with_inputs() {
        let mut input = parse_quote!(
            async fn complex(#[shuttle_shared_db::Postgres] pool: PgPool) -> ShuttleTide {}
        );

        let actual = Loader::from_item_fn(&mut input).unwrap();
        let expected_ident: Ident = parse_quote!(__shuttle_complex);
        let expected_inputs: Vec<Input> = vec![Input {
            ident: parse_quote!(pool),
            builder: Builder {
                path: parse_quote!(shuttle_shared_db::Postgres),
                options: Default::default(),
            },
        }];

        assert_eq!(actual.fn_ident, expected_ident);
        assert_eq!(actual.fn_inputs, expected_inputs);

        // Make sure attributes was removed from input
        if let syn::FnArg::Typed(param) = input.sig.inputs.first().unwrap() {
            assert!(
                param.attrs.is_empty(),
                "some attributes were not removed: {:?}",
                param.attrs
            );
        } else {
            panic!("expected first input to be typed")
        }
    }

    #[test]
    fn output_with_inputs() {
        let input = Loader {
            fn_ident: parse_quote!(__shuttle_complex),
            fn_inputs: vec![
                Input {
                    ident: parse_quote!(pool),
                    builder: Builder {
                        path: parse_quote!(shuttle_shared_db::Postgres),
                        options: Default::default(),
                    },
                },
                Input {
                    ident: parse_quote!(redis),
                    builder: Builder {
                        path: parse_quote!(shuttle_shared_db::Redis),
                        options: Default::default(),
                    },
                },
            ],
            fn_return: parse_quote!(ShuttleComplex),
        };

        let actual = quote!(#input);
        let expected = quote! {
            async fn loader(
                mut factory: shuttle_runtime::ProvisionerFactory,
                mut resource_tracker: shuttle_runtime::ResourceTracker,
            ) -> ShuttleComplex {
                use shuttle_runtime::Context;
                use shuttle_runtime::{Factory, ResourceBuilder};
                let pool = shuttle_runtime::get_resource(
                    shuttle_shared_db::Postgres::new(),
                    &mut factory,
                    &mut resource_tracker,
                ).await.context(format!("failed to provision {}", stringify!(shuttle_shared_db::Postgres)))?;
                let redis = shuttle_runtime::get_resource(
                    shuttle_shared_db::Redis::new(),
                    &mut factory,
                    &mut resource_tracker,
                ).await.context(format!("failed to provision {}", stringify!(shuttle_shared_db::Redis)))?;

                __shuttle_complex(pool, redis).await
            }
        };

        assert_eq!(actual.to_string(), expected.to_string());
    }

    #[test]
    fn parse_builder_options() {
        let input: BuilderOptions = parse_quote!(
            string = "string_val",
            boolean = true,
            integer = 5,
            float = 2.65,
            enum_variant = SomeEnum::Variant1,
            sensitive = "user:{secrets.password}"
        );

        let mut expected: BuilderOptions = Default::default();
        expected.options.push(parse_quote!(string = "string_val"));
        expected.options.push(parse_quote!(boolean = true));
        expected.options.push(parse_quote!(integer = 5));
        expected.options.push(parse_quote!(float = 2.65));
        expected
            .options
            .push(parse_quote!(enum_variant = SomeEnum::Variant1));
        expected
            .options
            .push(parse_quote!(sensitive = "user:{secrets.password}"));

        assert_eq!(input, expected);
    }

    #[test]
    fn from_with_input_options() {
        let mut input = parse_quote!(
            async fn complex(
                #[shared::Postgres(size = "10Gb", public = false)] pool: PgPool,
            ) -> ShuttlePoem {
            }
        );

        let actual = Loader::from_item_fn(&mut input).unwrap();
        let expected_ident: Ident = parse_quote!(__shuttle_complex);
        let mut expected_inputs: Vec<Input> = vec![Input {
            ident: parse_quote!(pool),
            builder: Builder {
                path: parse_quote!(shared::Postgres),
                options: Default::default(),
            },
        }];

        expected_inputs[0]
            .builder
            .options
            .options
            .push(parse_quote!(size = "10Gb"));
        expected_inputs[0]
            .builder
            .options
            .options
            .push(parse_quote!(public = false));

        assert_eq!(actual.fn_ident, expected_ident);
        assert_eq!(actual.fn_inputs, expected_inputs);
    }

    #[test]
    fn output_with_input_options() {
        let mut input = Loader {
            fn_ident: parse_quote!(complex),
            fn_inputs: vec![Input {
                ident: parse_quote!(pool),
                builder: Builder {
                    path: parse_quote!(shuttle_shared_db::Postgres),
                    options: Default::default(),
                },
            }],
            fn_return: parse_quote!(ShuttleComplex),
        };

        input.fn_inputs[0]
            .builder
            .options
            .options
            .push(parse_quote!(size = "10Gb"));
        input.fn_inputs[0]
            .builder
            .options
            .options
            .push(parse_quote!(public = false));

        let actual = quote!(#input);
        let expected = quote! {
            async fn loader(
                mut factory: shuttle_runtime::ProvisionerFactory,
                mut resource_tracker: shuttle_runtime::ResourceTracker,
            ) -> ShuttleComplex {
                use shuttle_runtime::Context;
                use shuttle_runtime::{Factory, ResourceBuilder};
                let vars = std::collections::HashMap::from_iter(factory.get_secrets().await?.into_iter().map(|(key, value)| (format!("secrets.{}", key), value)));
                let pool = shuttle_runtime::get_resource (
                    shuttle_shared_db::Postgres::new().size(&shuttle_runtime::strfmt("10Gb", &vars)?).public(false),
                    &mut factory,
                    &mut resource_tracker,
                ).await.context(format!("failed to provision {}", stringify!(shuttle_shared_db::Postgres)))?;
                std::mem::drop(vars);

                complex(pool).await
            }
        };

        assert_eq!(actual.to_string(), expected.to_string());
    }

    #[test]
    fn ui() {
        let t = trybuild::TestCases::new();
        t.compile_fail("tests/ui/main/*.rs");
    }
}
```
### Result
```
No clear performance improvements found.
```

# Go Examples

## Example 1:

### Code Snippet:
```
package risk

import (
	"sync"

	"github.com/DataDog/KubeHound/pkg/kubehound/models/store"
	"github.com/DataDog/KubeHound/pkg/telemetry/log"
)

var engineInstance *RiskEngine
var riOnce sync.Once

// Engine returns the risk engine singleton instance.
func Engine() *RiskEngine {
	var err error
	riOnce.Do(func() {
		engineInstance, err = newEngine()
		if err != nil {
			log.I.Fatalf("Risk engine initialization: %v", err)
		}
	})

	return engineInstance
}

// RiskEngine computes which assets are deemed critical based on a set of pre-configured rules.
type RiskEngine struct {
	roleMap map[string]bool // Map of critical roles
}

// newEngine creates a new risk engine instance. Should not be called directly.
func newEngine() (*RiskEngine, error) {
	return &RiskEngine{
		roleMap: CriticalRoleMap,
	}, nil
}

// IsCritical reports whether the provided asset should be marked as critical.
// The function expects a single store model input and currently only supports Roles.
func (ra *RiskEngine) IsCritical(model any) bool {
	switch o := model.(type) {
	case *store.PermissionSet:
		if ra.roleMap[o.RoleName] && !o.IsNamespaced {
			return true
		}
	}

	return false
}
```
### Result
```
No clear performance improvements found.
```

## Example 2:

### Code Snippet:
```
func AddressType(address string) (discoveryv1.AddressType, error) {
	ip := net.ParseIP(address)
	switch {
	case ip.To4() != nil:
		return discoveryv1.AddressTypeIPv4, nil
	case ip.To16() != nil:
		return discoveryv1.AddressTypeIPv6, nil
	}

	if match, _ := regexp.MatchString(AddressFQDNMatcher, address); match {
		return discoveryv1.AddressTypeFQDN, nil
	}

	return "", fmt.Errorf("invalid addrress input: %s", address)
}
```
### Result
```
No clear performance improvements found.
```

## Example 3:

### Code Snippet:
```
func printValidate(filename string, verbose bool) error {
	filenames, err := gatherFilenames(filename)
	if err != nil {
		return err
	}
	fileWalker := migrationstatsos.NewFileWalker(filenames...)
	stats, err := migrationstats.GatherStats(fileWalker, false)
	if err != nil {
		return err
	}
	// TODO(mf): we should introduce a --debug flag, which allows printing
	// more internal debug information and leave verbose for additional information.
	if !verbose {
		return nil
	}
	w := tabwriter.NewWriter(os.Stdout, 0, 0, 3, ' ', tabwriter.TabIndent)
	fmtPattern := "%v\t%v\t%v\t%v\t%v\t\n"
	fmt.Fprintf(w, fmtPattern, "Type", "Txn", "Up", "Down", "Name")
	fmt.Fprintf(w, fmtPattern, "────", "───", "──", "────", "────")
	for _, m := range stats {
		txnStr := "✔"
		if !m.Tx {
			txnStr = "✘"
		}
		fmt.Fprintf(w, fmtPattern,
			strings.TrimPrefix(filepath.Ext(m.FileName), "."),
			txnStr,
			m.UpCount,
			m.DownCount,
			filepath.Base(m.FileName),
		)
	}
	return w.Flush()
}
```
### Result
```
No clear performance improvements found.
```

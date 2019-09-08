# coinofflinewallet
Use Raspberry Pi for Cold Wallet

EXPERIMENTAL CODE: DO NOT USE ON LIVE WALLETS, YOU HAVE BEEN WARNED!!!

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

To use the code you will need a computer with an internet connection and a second computer that is airgapped (Raspberry Pi).

Both computers should have the wallet of the coin you want to use installed, the private keys are kept on the airgapped machine and this does not need sychronization with the block-chain.

Code relies on the API from https://chainz.cryptoid.info/api.dws, you can apply for an API Key there.

The wallets on both computers must have the RPC server enabled with "server=1" and "rpcuser=" and "rpcpassword=" set in the .conf file.

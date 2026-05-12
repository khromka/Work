#include &lt;windows.h&gt;
#include &lt;iostream&gt;
#include &lt;math.h&gt;
using namespace std;
int main() {
SetConsoleCP(1251);
SetConsoleOutputCP(1251);

float a = 2, b = 4, h = 0.5, x, y;
cout &lt;&lt; &quot;Обчислення функції y:\n&quot;;
for (x = a; x &lt;= b; x += h)
{
double f_x = 1 / (1 + pow(sin(x), 2));
cout &lt;&lt; &quot;f(&quot; &lt;&lt; x &lt;&lt; &quot;) = &quot; &lt;&lt; f_x &lt;&lt; endl;

}
return 0;
}

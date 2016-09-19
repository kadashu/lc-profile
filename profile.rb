#!/usr/bin/env ruby
#
# gem install descriptive_statistics
#
require 'open3'
require 'json'
require 'descriptive_statistics'

LC_APP_ID    = ENV['LC_APP_ID']
LC_MASTER_KEY= ENV['LC_MASTER_KEY']
task   =  ARGV[0]  || 'fixme'
count  = ( ARGV[1] || 10 ).to_i
result = { 'stdout' => [] }
failed = 0
tasks  = {
  'ping' => { 'method' => 'GET', 'path' => 'ping', 'accpet_http_code' => /^200$/ },
  'create_conversation' => { 'method' => 'POST', 'path' => 'classes/_Conversation', 'data' => '{"name":"My Private Room in Test","m":[]}', 'accept_http_code' => /^2[0-9]+$/, 'auth' => true, 'json' => true }
}

puts "count #{count}"
if not tasks.has_key? task
  puts "available task: #{tasks.keys}"
  exit 1
end

def format_cmd( ctask)
  cmd = "curl -s -X #{ctask['method']} -w 'nslookup: %{time_namelookup}, connect: %{time_connect}, init_ssl: %{time_appconnect}, pretransfer: %{time_pretransfer}, starttransfer: %{time_starttransfer}, total_time: %{time_total}, http_code: %{http_code} \n' https://api.leancloud.cn/1.1/#{ctask['path']} -o /dev/null"
  cmd = cmd + " -d '#{ctask['data']}'" if ctask.has_key? 'data'
  cmd = cmd + ' -H "Content-Type: application/json"' if ctask['json'] == true
  cmd = cmd + " -H 'X-LC-Id: #{LC_APP_ID}' -H 'X-LC-Key: #{LC_MASTER_KEY}'" if ctask['auth'] == true
  return cmd
end

count.downto 1 do | x |
  print '.'
  ctask = tasks[ task ]
  cmd   = format_cmd( ctask )
  out, err, status = Open3.capture3( cmd )
  if status.success?
    # nslookup: 0.520, connect: 0.556, init_ssl: 0.750, pretransfer: 0.750, starttransfer: 0.786, total_time: 0.786, http_code: 200
    frag = {}
    out.split(',').map { | e | frag[ e.split(':').first.strip ] = e.split(':').last.to_f }
    if ctask.has_key? 'accept_http_code'
      next if not frag['http_code'].to_i.to_s =~ ctask['accept_http_code']
    end
    result['stdout'].push( out.chomp.gsub(' ','') )
    frag.each do | k, v |
      next if k == 'http_code'
      result[ k ] = [] if not result.has_key? k
      result[ k ].push( v )
    end
  else
    failed +=1
    puts "\n#{err}\n"
  end
end

puts "\nfailed request: #{failed}\n"
puts result.to_json
result.map { | k, v | puts "
 #{k} count: #{v.number}
 min:  #{v.min}
 max:  #{v.max}
 mean: #{v.mean}
 p90:  #{v.percentile(90)}
 p95:  #{v.percentile(95)}
 p99:  #{v.percentile(99)}" if k !~ /(http_code|stdout)/
}
